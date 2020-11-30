from utility_readingfiles.testcsv import Testcsv
from config_validation_resultsreport.tablecreation import TbToValidate
from baseconfig_dataProfiling.dataprofiling_base import profilingBase
from validationrules.validation import Validation
from config_validation_resultsreport.testresult import TestResult
from utility_readingfiles.utility_testRunner import utility_testRunner
import allure
import pytest


@pytest.fixture()
def csv_source_s1():
    s1_file_location = 'input_filerepository/csv/csv_s1.csv'
    test_source = utility_testRunner()
    test_source.read_datasource(s1_file_location)
    return test_source.read_datasource(s1_file_location)


@allure.feature('test_module_01')
@allure.story('test_story_01')
@allure.severity('normal')
@pytest.mark.run(order=1)
def test_source_profiling_tc01(csv_source_s1):
    """
        Use case description: This is a use case description, Test case 01, Data profiling of csv_s1.csv file
    """
    profiling_tc01 = profilingBase(csv_source_s1)
    profiling_tc01.sourcedataprofiling()


@allure.feature('test_module_01')
@allure.story('test_story_02')
@allure.severity('critical')
@pytest.mark.run(order=2)
def test_source_csv_general(csv_source_s1):
    result = Validation().run_validation_on(csv_source_s1).expect_column_values_to_be_unique("ID", "Test - Unique value for ID")\
                                                          .expect_column_values_to_not_be_null("ID", "Test - No Null values for ID")\
                                                          .expect_column_value_lengths_to_equal("Name", 4, "Test - Name length is 4")\
                                                          .expect_column_values_to_be_of_type("Name", "object", "Test - Name data type is String only")\
                                                          .expect_column_values_to_be_in_set("Gender", ["M", "F"], "Test - Gender values in List")\
                                                          .expect_column_values_to_match_regex("Email", "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)", "Test - Email format check")\
                                                          .get_results()
    """
        Use case description: This is a use case description, Test case 02, Validate business requirements against the values in data file 
    """
    # perform PYTest Assertion
    assert TestResult().is_test_passed(result) == 'True'


@allure.feature('test_module_01')
@allure.story('test_story_03')
@allure.severity('critical')
@pytest.mark.run(order=3)
def test_source_csv_business_validation(csv_source_s1):
    csv_source_selection = csv_source_s1[(csv_source_s1.Age > 75)]
    result = Validation().run_validation_on(csv_source_selection).expect_table_row_count(0, "More than 75 years old") \
                                                                 .get_results()
    """
        Use case description: This is a use case description, Test case 03, Validate the number of Age values exceeding the expected limit of 75
    """
    # perform PYTest Assertion
    assert TestResult().is_test_passed(result) == 'True'


@pytest.fixture()
def csv_source_s2():
    s2_file_location = 'input_filerepository/csv/csv_s2.csv'
    test_source = utility_testRunner()
    test_source.read_datasource(s2_file_location)
    return test_source.read_datasource(s2_file_location)


@allure.feature('test_module_02')
@allure.story('test_story_01')
@allure.severity('critical')
@pytest.mark.run(order=4)
def test_source_target_comparison(csv_source_s1, csv_source_s2):
    comparison = Validation().compare_table1_values_with_table2_values(csv_source_s1, csv_source_s2)
    """
        Use case description: This is a use case description, Data comparison test of csv_s1.csv & csv_s2.csv        
    """
    # perform pytest assertion
    assert comparison == (0, 'True', 'True')


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', 'allure_results/json'])
