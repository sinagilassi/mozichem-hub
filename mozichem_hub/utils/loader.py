# import libs
import os
import yaml
from typing import Dict, List
# local
from ..config import app_settings


class Loader:

    def __init__(self):
        """
        Initialize the Reference instance.
        """
        # data path
        # self.data_dir = app_settings.data_dir

    def load_yml_references(
        self,
        target_folder: str,
        target_file: str
    ) -> Dict:
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
            # NOTE: check if target_folder and target_file are provided
            if not target_folder or not target_file:
                raise ValueError(
                    "Both target_folder and target_file must be provided.")

            # target file format
            if not target_file.endswith('.yml'):
                raise ValueError("The target_file must be a .yml file.")

            # NOTE: get the current folder and parent folder
            # current folder relative
            current_folder = os.path.dirname(__file__)
            # parent folder
            parent_folder = os.path.dirname(current_folder)
            # data folder
            data_folder = os.path.join(parent_folder, target_folder)
            # reference yml file
            reference_file = os.path.join(data_folder, target_file)

            # NOTE: check file exists
            if os.path.exists(reference_file):
                # load yml
                with open(reference_file, 'r') as f:
                    ref = yaml.load(f, Loader=yaml.FullLoader)

                    return ref['REFERENCES']
            else:
                raise Exception('Reference file not found!')
        except Exception as e:
            raise Exception('Loading reference failed! ', e)

    def list_yml_references(
        self,
        target_folder: str
    ) -> Dict[str, str]:
        """
        List all yml files in the specified folder.

        Parameters
        ----------
        target_folder : str
            The folder to list yml files from.

        Returns
        -------
        Dict[str, str]
            A dictionary with file names as keys and their paths as values.
        """
        try:
            # NOTE: get the current folder and parent folder
            # current folder relative
            current_folder = os.path.dirname(__file__)
            # parent folder
            parent_folder = os.path.dirname(current_folder)
            # data folder
            data_folder = os.path.join(parent_folder, target_folder)

            # list all yml files in the target folder
            yml_files = {
                file_name: os.path.join(data_folder, file_name)
                for file_name in os.listdir(data_folder) if file_name.endswith('.yml')
            }

            return yml_files
        except Exception as e:
            raise Exception('Listing yml references failed! ', e) from e

    def load_all_yml_references(
        self,
        target_folder: str = 'descriptors'
    ) -> Dict[str, Dict]:
        """
        Load all yml references from the specified folder.

        Parameters
        ----------
        target_folder : str
            The folder to load yml references from.

        Returns
        -------
        Dict[str, Dict]
            A dictionary with file names as keys and their contents as values.
        """
        try:
            # list all yml files in the target folder
            yml_files = self.list_yml_references(target_folder)

            # load each yml file
            references = {}
            for file_name, file_path in yml_files.items():
                with open(file_path, 'r') as f:
                    references[file_name] = yaml.load(
                        f, Loader=yaml.FullLoader)

            return references
        except Exception as e:
            raise Exception('Loading all yml references failed! ', e) from e
