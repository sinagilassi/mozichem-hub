# import libs
import os
import yaml
from typing import Dict
# local
from ..config import app_settings


class ToolsReferences:

    def __init__(self):
        """
        Initialize the Reference instance.
        """
        # data path
        # self.data_dir = app_settings.data_dir

    def load_references(self):
        '''
        Load references yml files having details about tools and their parameters.

        Parameters
        ----------
        None

        Returns
        -------
        reference : dict
            reference yml files
        '''
        try:
            # current folder relative
            current_folder = os.path.dirname(__file__)
            # parent folder
            parent_folder = os.path.dirname(current_folder)
            # data folder
            data_folder = os.path.join(parent_folder, 'data')
            # reference yml file
            reference_file = os.path.join(data_folder, 'references.yml')

            # check file exists
            if os.path.exists(reference_file):
                # load yml
                with open(reference_file, 'r') as f:
                    ref = yaml.load(f, Loader=yaml.FullLoader)

                    return ref['REFERENCES']
            else:
                raise Exception('Reference file not found!')
        except Exception as e:
            raise Exception('Loading reference failed! ', e)

    def select_reference(self, name):
        '''
        Select reference yml file

        Parameters
        ----------
        name: str
            reference name

        Returns
        -------
        reference : dict
            selected reference yml file
        '''
        try:
            # reference
            reference = self.load_references()
            # selected reference
            return reference[name]
        except Exception as e:
            raise Exception('Selecting reference failed! ', e)
