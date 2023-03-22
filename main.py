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

#Reading the file in s3
def read_plots_input(s3,bucket_name, file):
    # Create an S3 access object
    obj = s3.Object(bucket_name, file)
    data = obj.get()['Body'].read()
    logging.info(f"""--- Match of fields {data.decode("utf-8")} ---""")
    with BytesIO(data) as bio:
        df = pd.read_csv(bio)
    return df

def _write_dataframe_to_csv_on_s3(DESTINATION, dataframe, filename, s3_resource):
    """ Write a dataframe to a CSV on S3 """
    logging.info(
        "Writing {} records to '{}' in bucket '{}'.".format(
            len(dataframe), filename, DESTINATION
        )
    )
    # Create buffer
    csv_buffer = StringIO()
    # Write dataframe to buffer
    dataframe.to_csv(csv_buffer, sep=",", index=False)
    # Create S3 object
    # Write buffer to S3 object
    s3_resource.Object(DESTINATION, filename).put(Body=csv_buffer.getvalue())

def input_enginering(s3_resource, inputfile, OUTPUTBUCKET, folder, filename):
    print('Here in input enginering ', inputfile.columns)
    for i in ['plot_id', 'size', 'Region Names']:
        if i not in inputfile.columns:
            print('Noooooooo>>> ', i)
    df_gb0 = inputfile.groupby(['plot_id', 'size', 'Region Names'], as_index=False).agg({
        'WoodsExistence': ['sum'],
        'StonesExistence': ['sum'],
        'FabricsExistence': ['sum'],
        'MetalsExistence': ['sum'],
        'GemsExistence': ['sum'],
        'ElementExistence': ['sum']})

    df_gb0.columns = [x[0] if 'Existence' not in x[0] else
                      x[0][:-9] + '__Deposits' for x in df_gb0.columns.ravel()]

    df_gb0['Deposits'] = df_gb0['Woods__Deposits'] + df_gb0['Stones__Deposits'] + df_gb0['Fabrics__Deposits'] + df_gb0[
        'Metals__Deposits'] + df_gb0['Gems__Deposits'] + df_gb0['Element__Deposits']
    df_gb0['Percentile_Deposits_Rank'] = df_gb0.Deposits.rank(pct=True)

    _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_gb0,
                                  folder + os.environ['INPUTFILE'][:10].replace(' ','')+filename, s3_resource)

def classification(x):
    classif = 'Bountiful'
    if x<.10:
        classif = 'Meager'
    elif x<.35:
        classif = 'Fair'
    elif x<.65:
        classif = 'Rich'
    elif x<.91:
        classif = 'Lush'
    return classif

def deposits_score(s3_resource, inputfile, OUTPUTBUCKET, folder):
    print('Here in input deposit scores ', inputfile.columns)
    for i in ['plot_id', 'size', 'Region Names']:
        if i not in inputfile.columns:
            print('Noooooooo 11>>> ', i)
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
        df_gb[i + '_existence_rank'] = df_gb[i + '_repeated'].rank(method='dense')

    df_gb['Existence_puntuation_mult'] = df_gb['Woods_existence_rank'] * df_gb['Stone_existence_rank'] * df_gb[
        'Fabrics_existence_rank'] * df_gb['Metals_existence_rank'] * df_gb['Gems_existence_rank'] * df_gb[
                                              'Element_existence_rank']

    df_gb['Existence_percentile_mult'] = df_gb.Existence_puntuation_mult.rank(pct=True)

    df_gb['Existence_AvgRank_mult'] = df_gb[['Existence_percentile_mult', 'Percentile_Deposits_Rank']].mean(axis=1)
    df_gb['Pctile_DepositExistence'] = df_gb.Existence_AvgRank_mult.rank(pct=True)
    df_gb['Class_Deposits_mult'] = df_gb['Pctile_DepositExistence'].apply(lambda x: classification(x))

    _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_gb,
                                  folder + os.environ['INPUTFILE'][:10].replace(' ','')+'_deposits_score.csv',s3_resource)


def intensity_score(s3_resource, inputfile, OUTPUTBUCKET):
    print('Here in intensity_score ', inputfile.columns)
    for i in ['plot_id', 'size', 'Region Names']:
        if i not in inputfile.columns:
            print('Noooooooo>>> ', i)

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
    _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_base,
                                'output/' +os.environ['INPUTFILE'][:10].replace(' ','')+ '_intensity_score.csv', s3_resource)


def prev_intensity_score(s3_resource, inputfile, OUTPUTBUCKET, folder):
    print('Here in prev_intensity_score ', inputfile.columns)
    for i in ['plot_id', 'size', 'Region Names']:
        if i not in inputfile.columns:
            print('Noooooooo 11>>> ', i)

    df_base = inputfile[['plot_id', 'size', 'Region Names']].drop_duplicates()

    newcols = []
    for i in range(0, 6):
        new = inputfile.pivot(index='plot_id', columns=[family[i]], values=family[i] + '_Full_Intensity')
        new.columns = [x + '_tintensity' for x in new.columns.ravel()]
        newcols.append([x for x in new.columns.ravel()])
        df_base = df_base.merge(new, on=['plot_id'], how='left')
        #dfames.append(new)
    _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_base,
                        folder +os.environ['INPUTFILE'][:10].replace(' ','')+'_prev_intensity_score_salida_1.csv', s3_resource)



    for i in df_base.columns[3:]:
        dict_tam = {}
        dups_color = df_base.pivot_table(columns=[i], aggfunc='size')
        for key, value in dups_color.iteritems():
            if int(key) < 10:
                dict_tam[key] = value * (11 - int(key))
            else:
                dict_tam[key] = value

        df_base[i + '_repeated'] = df_base[i].map(dict_tam)
        df_base[i + '_tintensity_rank_prev'] = df_base[i + '_repeated'].rank(method='dense')
        df_base[i + '_tintensity_rank'] = df_base[i + '_tintensity_rank_prev'].rank(pct=True)


    _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_base,
                    folder + os.environ['INPUTFILE'][:10].replace(' ','')+'_prev_intensity_score_salida_2.csv', s3_resource)

    intensity_score(s3_resource, df_base, 'score/')
    print('Ok on intensity score')

def unique_score(a,b):
    mfin2 = a.merge(b, on=['plot_id'], how='left')
    mfin2['weighted_puntuation'] = (os.environ['WEIGH_INTENS'] * mfin2['Percentile_IntensityAccumulated']) + \
                                (os.environ['WEIGH_DE'] * mfin2['Pctile_DepositExistence'])
    mfin2['pctil_final_puntuation'] = mfin2.weighted_puntuation.rank(pct=True)
    mfin2['Class_final_puntuation'] = mfin2['pctil_final_puntuation'].apply(lambda x: classification(x))

    _write_dataframe_to_csv_on_s3(OUTPUTBUCKET, df_base, 'output/' + 'final_score.csv', s3_resource)

def main(event):
    print('Init by ', event)
    s3_resource = boto3.resource('s3', region_name=os.environ['AWSREGION_NAME'],
                                 aws_access_key_id=os.environ['AWSACCESS_KEY_ID'],
                                 aws_secret_access_key=os.environ['AWSSECRET_ACCESS_KEY'])
    bucket_input = os.environ['BUCKETNAME']
    bucket_output = os.environ['BUCKET-OUTPUT']
    file_resources = read_plots_input(s3_resource,bucket_input, 'plotresourcesoutput/'+os.environ['INPUTFILE'])
    print('Input columns ', file_resources.columns)
    print('Here in intensity_score ', file_resources.columns)
    for i in ['plot_id', 'size', 'Region Names']:
        if i not in file_resources.columns:
            print('Noooooooo>>> ', i)

    deposits_score(s3_resource, file_resources, bucket_output, 'auxiliar/')
    prev_intensity_score(s3_resource, file_resources, bucket_output, 'auxiliar/')

    deposit_score_file = read_plots_input(s3_resource,bucket_output,
                                'output/'+os.environ['INPUTFILE'][:10].replace(' ','')+ '_deposits_score.csv')
    intensities_score_file = read_plots_input(s3_resource,bucket_output,
                                'output/'+os.environ['INPUTFILE'][:10].replace(' ','')+ '_intensity_score.csv')
    unique_score(deposit_score_file, intensities_score_file)
    logger.info('Here ok')


event={'file':'plots_QA (2)_salida_2.csv'}
main(event)