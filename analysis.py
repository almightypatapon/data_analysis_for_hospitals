import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def merge_data(path, files):
    merged_df = None

    for i, file in enumerate(files):
        if i == 0:
            merged_df = pd.read_csv(path + file)
        else:
            data = pd.read_csv(path + file)
            data.columns = merged_df.columns
            merged_df = pd.concat([merged_df, data], ignore_index=True)
    return merged_df


def clear_data(df):
    df.drop(columns=['Unnamed: 0'], inplace=True)
    df.dropna(axis=0, how='all', inplace=True)  # merge_date.drop(index=merge_date[merge_date.isna().all(axis=1)].index, inplace=True)
    df.gender = df.gender.str.replace(r'(female|woman)', 'f', regex=True)
    df.gender = df.gender.str.replace(r'(male|man)', 'm', regex=True)
    df.gender = df.gender.fillna('f')
    return df.fillna(0)


def get_data_count(df, blood_test=False):
    blood_tests = {}
    for hospital in df.hospital.unique():
        blood_tests[hospital] = df.loc[(df.hospital == hospital) & (df.blood_test == 't' if blood_test else True)].shape[0]
    return blood_tests


def share_of_patients(df, hospital, diagnosis):
    diagnosis_count = df.loc[(df.hospital == hospital) & (df.diagnosis == diagnosis)].shape[0]
    return round(diagnosis_count / get_data_count(df)[hospital], 3)


def get_median(df, hospital, column):
    return df.loc[df.hospital == hospital][column].median()


def answers_stage4(df):
    answers = {}
    patients = get_data_count(df)
    answers['1st'] = (max(patients, key=lambda x: patients[x]))
    answers['2nd'] = share_of_patients(df, 'general', 'stomach')
    answers['3rd'] = share_of_patients(df, 'sports', 'dislocation')
    answers['4rd'] = round(get_median(df, 'general', 'age') - get_median(df, 'sports', 'age'))
    blood_tests_taken = get_data_count(df, True)
    answers['5th'] = [f'{key}, {value} blood tests' for key, value in blood_tests_taken.items() if value == max(blood_tests_taken.values())][0]
    return answers


def print_answers(answers):
    for key, value in answers.items():
        print(f'The answer to the {key} question: {value}')


def answers_stage5():
    answers = {'1st': '15 - 35', '2nd': 'pregnancy',
               '3rd': "It's because the sports hospital uses imperial units where the others use metric"}
    return answers


files_path = r'test/'
input_files = ['general.csv', 'prenatal.csv', 'sports.csv']
hospitals_data = merge_data(files_path, input_files)
hospitals_data = clear_data(hospitals_data)
print_answers(answers_stage5())

hospitals_data.plot(y='age', kind='hist')
plt.show()
hospitals_data.diagnosis.value_counts().plot(kind='pie')
plt.show()
# hospitals_data.plot(y=['height'], kind='box', showmeans=True)
sns.violinplot(x=hospitals_data.hospital, y=hospitals_data.height, hue=hospitals_data.gender, split=True, inner='quartile')
plt.show()
