from io import BytesIO
import pandas as pd
import logging
import boto3
import os

from io import StringIO # python3; python2: BytesIO

N = 13000
def fxy(x):
    if x<.5:
        return 0
    else:
        return N / x

family = ['Woods', 'Stone', 'Fabrics','Metals', 'Gems', 'Element']
ifile = 'plots_PROD (2).csv'
def classification(x):
    classif = 'Bountiful'
    if x<.05:
        classif = 'Meager'
    elif x<.3:
        classif = 'Fair'
    elif x<.7:
        classif = 'Rich'
    elif x<.95:
        classif = 'Lush'
    return classif
def read_plots_input(s3,bucket_name, file):
    # Create an S3 access object
    obj = s3.Object(bucket_name, file)
    data = obj.get()['Body'].read()
    logging.info(f"""--- Match of fields {data.decode("utf-8")} ---""")
    with BytesIO(data) as bio:
        df = pd.read_csv(bio)
    return df


def _write_dataframe_to_csv_on_s3(DESTINATION, dataframe, filename):
    """ Write a dataframe to a CSV on S3 """
    print(
        "Writing {} records to '{}' in bucket '{}'.".format(
            len(dataframe), filename, DESTINATION
        )
    )
    # Create buffer
    s3 = boto3.resource('s3', region_name=os.environ['AWSREGION_NAME'],
                                     aws_access_key_id=os.environ['AWSACCESS_KEY_ID'],
                                     aws_secret_access_key=os.environ['AWSSECRET_ACCESS_KEY'])
    try:
        csv_buffer = StringIO()
        dataframe.to_csv(csv_buffer, sep=",", index=False)
        s3.Object(DESTINATION, filename).put(Body=csv_buffer.getvalue())

        print('ok uploading ', filename)
    except Exception as e:
        logging.error('Error uploading ',e)


def deposits_score(inputfile, OUTPUTBUCKET, folder):
    logging.info('Here in input deposit scores ', inputfile.columns)
    try:
        df_gb = inputfile.groupby(['plot_id', 'size', 'Region Names'], as_index=False).agg({
            'WoodsExistence': ['sum'],
            'StoneExistence': ['sum'],
            'FabricsExistence': ['sum'],
            'MetalsExistence': ['sum'],
            'GemsExistence': ['sum'],
            'ElementExistence': ['sum']})

        df_gb.columns = [x[0] if 'Existence' not in x[0] else x[0][:-9] + '__Deposits' for x in df_gb.columns.ravel()]
        df_gb['Deposits'] = df_gb['Woods__Deposits'] + df_gb['Stone__Deposits'] + df_gb['Fabrics__Deposits'] + df_gb[
            'Metals__Deposits'] + df_gb['Gems__Deposits'] + df_gb['Element__Deposits']
        df_gb['Percentile_Deposits_Rank'] = df_gb.Deposits.rank(pct=True)

        for i in family:
            dict_tam = {}
            cols = i + '__Deposits'
            dep = i + '__Deposits'
            dups_color = df_gb.pivot_table(columns=[cols], aggfunc='size')
            for key, value in dups_color.iteritems():
                dict_tam[key] = value
                if key == 0:
                    dict_tam[key] = pow(value, 2)
                else:
                    if key < 2:
                        dict_tam[key] = pow(value, 1.5)
                    else:
                        if key < 3:
                            dict_tam[key] = pow(value, 1)
                        if key < 4:
                            dict_tam[key] = value * pow(N, 0.1)
                        else:
                            dict_tam[key] = value

            df_gb[i + '_repeated'] = df_gb[dep].map(dict_tam)
            df_gb[i + '_existence_rank_prev'] = df_gb[i + '_repeated'].apply(lambda x: fxy(x))
            df_gb[i + '_existence_rank'] = df_gb[i + '_existence_rank_prev'].rank(pct=True)
            #rank(method='dense')

        df_gb['Existence_puntuation_mult'] = df_gb['Woods_existence_rank'] * df_gb['Stone_existence_rank'] * df_gb[
            'Fabrics_existence_rank'] * df_gb['Metals_existence_rank'] * df_gb['Gems_existence_rank'] * df_gb[
                                                  'Element_existence_rank']

        df_gb['Existence_percentile_mult'] = df_gb.Existence_puntuation_mult.rank(pct=True)

        df_gb['Existence_AvgRank_mult'] = df_gb[['Existence_percentile_mult', 'Percentile_Deposits_Rank']].mean(axis=1)
        df_gb['Pctile_DepositExistence'] = df_gb.Existence_AvgRank_mult.rank(pct=True)
        df_gb['Class_Deposits_mult'] = df_gb['Pctile_DepositExistence'].apply(lambda x: classification(x))

        _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_gb,
                                      folder + os.environ['INPUTFILE'][:10].replace(' ','').replace('(','')+
                                      '_deposits_score.csv')
    except Exception as e:
        logging.error('Error on deposits existence ', e)

def intensity_score(inputfile, OUTPUTBUCKET):
    logging.info('Here in intensity_score ', inputfile.columns)
    try:
        df_gb0 = inputfile.copy()
        df_gb0['IntensityAccumulated'] = df_gb0['Ash_tintensity_rank'] * df_gb0['Holly_tintensity_rank'] * df_gb0[
            'Oak_tintensity_rank'] * df_gb0['Olive_tintensity_rank'] * df_gb0['Pine_tintensity_rank'] * df_gb0[
                                             'Redwood_tintensity_rank'] * df_gb0['Willow_tintensity_rank'] * df_gb0[
                                             'Alabaster_tintensity_rank'] * df_gb0['Basalt_tintensity_rank'] * df_gb0[
                                             'Granite_tintensity_rank'] * df_gb0['Limestone_tintensity_rank'] * df_gb0[
                                             'Marble_tintensity_rank'] * df_gb0['Sand_tintensity_rank'] * df_gb0[
                                             'Shale_tintensity_rank'] * df_gb0['Cashmere_tintensity_rank'] * df_gb0[
                                             'Cotton_tintensity_rank'] * df_gb0['Flax_tintensity_rank'] * df_gb0[
                                             'Hemp_tintensity_rank'] * df_gb0['Jute_tintensity_rank'] * df_gb0[
                                             'Silk_tintensity_rank'] * df_gb0['Wool_tintensity_rank'] * df_gb0[
                                             'Aluminum_tintensity_rank'] * df_gb0['Copper_tintensity_rank'] * df_gb0[
                                             'Iron_tintensity_rank'] * df_gb0['Tin_tintensity_rank'] * df_gb0[
                                             'Titanium_tintensity_rank'] * df_gb0['Tungsten_tintensity_rank'] * df_gb0[
                                             'Zinc_tintensity_rank'] * df_gb0['Amethyst_tintensity_rank'] * df_gb0[
                                             'Diamond_tintensity_rank'] * df_gb0['Emerald_tintensity_rank'] * df_gb0[
                                             'Ruby_tintensity_rank'] * df_gb0['Sapphire_tintensity_rank'] * df_gb0[
                                             'Smoky Quartz_tintensity_rank'] * df_gb0['Topaz_tintensity_rank'] * df_gb0[
                                             'Antimony_tintensity_rank'] * df_gb0['Calcium_tintensity_rank'] * df_gb0[
                                             'Carbon_tintensity_rank'] * df_gb0['Hydrogen_tintensity_rank'] * df_gb0[
                                             'Nitrogen_tintensity_rank'] * df_gb0['Silicon_tintensity_rank'] * df_gb0[
                                             'Sulfur_tintensity_rank']

        df_gb0['Percentile_IntensityAccumulated'] = df_gb0.IntensityAccumulated.rank(pct=True)
        df_gb0['Class_IntensityAccumulated'] = df_gb0['Percentile_IntensityAccumulated'].apply(lambda x: classification(x))
        _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_gb0,
                                    'output/' +os.environ['INPUTFILE'][:10].replace(' ','').replace('(','')+
                                      '_intensity_score.csv')
        logging.info('ok on intensity score')
    except Exception as e:
        logging.error('Error on intensity score ', e)


def prev_intensity_score(inputfile, OUTPUTBUCKET, folder):
    logging.info('Here in prev_intensity_score ', inputfile.columns)
    df_base = inputfile[['plot_id', 'size', 'Region Names']].drop_duplicates()
    try:
        newcols = []
        for i in range(0, 6):
            new = inputfile.pivot(index='plot_id', columns=[family[i]], values=family[i] + '_Full_Intensity')
            new.columns = [x + '_tintensity' for x in new.columns.ravel()]
            newcols.append([x for x in new.columns.ravel()])
            df_base = df_base.merge(new, on=['plot_id'], how='left')
            #dfames.append(new)
        _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_base,
                            folder +os.environ['INPUTFILE'][:10].replace(' ','').replace('(','')+
                                      '_prev_intensity_score_salida_1.csv')

        for i in df_base.columns[3:]:
            dict_tam = {}
            dups_color = df_base.pivot_table(columns=[i], aggfunc='size')
            for key, value in dups_color.iteritems():
                if int(key) < 10:
                    dict_tam[key] = value * (11 - int(key))
                else:
                    dict_tam[key] = value

            df_base[i + '_repeated'] = df_base[i].map(dict_tam)
            df_base[i + '_rank_prev'] = df_base[i + '_repeated'].apply(lambda x: fxy(x))
            df_base[i + '_rank'] = df_base[i + '_rank_prev'].rank(pct=True)


        _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_base,
                        folder + os.environ['INPUTFILE'][:10].replace(' ','').replace('(','')+
                                      '_prev_intensity_score_salida_2.csv')

        intensity_score(df_base, OUTPUTBUCKET)
        logging.info('Ok on intensity score')
    except Exception as e:
        logging.error('Error on prev intensity score ', e)


def unique_score(a, b, OUTPUTBUCKET, weight_intensity):
    logging.info('Here on unique score')
    try:
        mfin2 = a.merge(b, on=['plot_id'], how='left')
        mfin2['weighted_puntuation'] = \
            float(weight_intensity) * mfin2['Percentile_IntensityAccumulated'] + \
            float(1 - weight_intensity) * mfin2['Pctile_DepositExistence']
        mfin2['pctil_final_puntuation'] = mfin2.weighted_puntuation.rank(pct=True)
        mfin2['Class_final_puntuation'] = mfin2['pctil_final_puntuation'].apply(lambda x: classification(x))

        _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, mfin2, 'output/' +
                                      ifile[:10].replace(' ', '').replace('(', '') + '_final_score.csv')
        logging.info('Unique Score ', 'output/' +
                     ifile[:10].replace(' ', '').replace('(', '') + '_final_score.csv')
    except Exception as e:
        logging.error('Error on unique_score score ', e)


def main(event):
    try:
        s3_resource = boto3.resource('s3', region_name='us-east-1',  # os.environ['AWSREGION_NAME'],
                                     aws_access_key_id='AKIAQRXNKUHINLAA2F76',  # os.environ['AWSACCESS_KEY_ID'],
                                     aws_secret_access_key='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')  # os.environ['AWSSECRET_ACCESS_KEY'])

        bucket_input = 'plot-resources-files'  # os.environ['BUCKETNAME']
        bucket_output = 'plot-rarity-score'  # os.environ['BUCKET-OUTPUT']
        file_resources = read_plots_input(s3_resource, bucket_input, 'plotresourcesoutput/' + event['file'])

        deposits_score(file_resources, bucket_output, 'output/')
        prev_intensity_score(file_resources, bucket_output, 'auxiliar/')
        logging.info('Reading files to join ')
        deposit_score_file = read_plots_input(s3_resource, bucket_output,
                                              'output/' + ifile[:10].replace(' ', '').replace('(',
                                                                                              '') + '_deposits_score.csv')
        intensities_score_file = read_plots_input(s3_resource, bucket_output,
                                                  'output/' + ifile[:10].replace(' ', '').replace('(',
                                                                                                  '') + '_intensity_score.csv')
        unique_score(deposit_score_file, intensities_score_file, bucket_output, .5)

        print('Here ok', len(file_resources))

    except Exception as e:
        logging.error('Error on main function ', e)
