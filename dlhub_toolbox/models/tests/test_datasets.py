from dlhub_toolbox.models.datasets import Dataset, TabularDataset

import unittest
import os


class TestModels(unittest.TestCase):

    maxDiff = None

    def test_dataset(self):
        m = Dataset().set_authors(["Ward, Logan"], ["University of Chicago"])\
            .set_title("Example dataset").add_alternate_identifier("10.11", "DOI")\
            .add_related_identifier("10.11", "DOI", 'IsDescribedBy')\
            .add_funding_reference("ANL LDRD", '1', 'ISNI', '201801', 'DLHub')
        self.assertEqual(m.to_dict(),
                         {"datacite":
                              {"creators": [{"givenName": "Logan", "familyName": "Ward",
                                             "affiliations": "University of Chicago"}],
                               "titles": ["Example dataset"],
                               "publisher": 'DLHub',
                               "fundingReferences": [{
                                   "awardNumber": "201801",
                                   "awardTitle": "DLHub",
                                   "funderIdentifier": {'funderIdentifier': '1',
                                                        'funderIdentifierType': 'ISNI'},
                                   "funderName": "ANL LDRD"
                               }],
                               "relatedIdentifiers": [{
                                   "relatedIdentifier": "10.11",
                                   "relatedIdentifierType": "DOI",
                                   "relationType": "IsDescribedBy"
                               }],
                               "alternateIdentifiers": [{
                                   "alternateIdentifier": "10.11",
                                   "alternateIdentifierType": "DOI"
                               }]}
                         })

    def test_tabular_dataset(self):
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test.csv'))
        m = TabularDataset(data_path)
        self.assertEqual({'x': {'name': 'x'}, 'y': {'name': 'y'}}, m.columns)

        # Add some nonsense
        m.set_title('Example dataset')
        m.mark_inputs(['x'])
        m.mark_labels(['y'])
        m.annotate_column('x', description='Input variable', units='cm')
        m.annotate_column('y', data_type='scalar')
        self.assertEqual(m.to_dict(), {"datacite": {"titles": ["Example dataset"],
                                                    "creators": [], "publisher": "DLHub"},
                                       "dataset": {"location": data_path, "columns": [
                                           {"name": "x", "description": "Input variable", "units": "cm"},
                                           {"name": "y", "data_type": "scalar"}],
                                                   "inputs": ["x"], "labels": ["y"],
                                                   "format": "csv", "read_options": {}}})


if __name__ == "__main__":
    unittest.main()