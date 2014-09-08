import os
import pandas as pd
import statsmodels.api as sm

def getFullDF():
    resultsDir = '/Users/faiyamrahman/Desktop/results/mass/method4'
    numIters = 0
    os.chdir(resultsDir)
    for resultsFile in os.listdir(resultsDir):
        if not resultsFile.endswith('xlsx'):
            continue
        print resultsFile
        numIters += 1
        df = pd.read_excel( resultsFile, sheetname='Meta', verify_integrity=True, 
                            parse_cols=
                             'C,' + # N 
                             'D,' + # P
                             'E,' + # minPA
                             'G,' + # minERA
                             'M,' + # doubleDown
                             'N')   # Mean(topFiveStreaks)
        if numIters == 1:
            newDF = df
            continue
        newDF = pd.concat([newDF, df], axis=0)
        # testing
    # newDF.to_excel(resultsDir + 'finished.xlsx', sheet_name='Meta', index=False)

    return newDF

def addQuadraticPColumn(df, alpha):
    df['Palpha'] = df.P.map(lambda p: ( ((p - alpha) ** 2) * -1) )
    # df['Palpha'] = df.P
    return df

def main():
    """
    Run a Multiple Linear Regression on simulation data for strategy 4
    """
    ## Import the data into a dataframe
    df = getFullDF() # Columns: N, P, minERA, doubleDown, Mean(topFiveStreaks)

    ## Parse the data to only include rows with
    df = df[ df['min PA'] == 100 ] # minPA == 500
    df = df[ df['DoubleDown?'] == True ] # doubleDown == True

    f = open('analysis.txt', "a+")

    ## Transform the P variable by a value alpha
    criticalValues = []
    for alpha in range(1,300):
        df = addQuadraticPColumn(df, alpha)

        ## Run the OLS
        X = df[['N', 'Palpha', 'min ERA']]
        y = df['Mean(topFiveStreaks)']
        results = sm.OLS(y, X).fit()

        ## print the data to file
        f.write('\n\n*************** Alpha: {} ***************\n'.format(alpha) )
        f.write( str(results.summary()) )
        f.write('\nB2 (Palpha): {}\n'.format(results.params.Palpha) )

        ## Save some data for later
        criticalValues.append( (alpha, 
                                round(results.rsquared, 4), 
                                results.params.Palpha))

    f.write('\n\n')
    f.write('*** THE CHAMPIONS *** \n')
    lCV = list(criticalValues)
    lCV.sort(key=lambda x: x[1], reverse=True)
    for alpha, rsquared, b2 in lCV:
        # if b2 < 0:
        f.write('alpha, R2, Palpha: {}, {}, {}\n'.format(alpha, rsquared, b2))

    f.close()

if __name__ == '__main__':
    main()