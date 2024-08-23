# Copyright (c) OpenMMLab. All rights reserved.
from typing import List, Optional, Union

from mmengine import fileio
from mmengine.logging import MMLogger

from mmpretrain.registry import DATASETS
from .categories import PLANT_ANOMALY_AREA
from .custom import CustomDataset

@DATASETS.register_module()
class PlantAnomalyArea(CustomDataset):
    """The insect plant dataset has following categories
    'K0', 'N0', 'OT07', 'OT10', 'rDA09', 'rDB01', 'rDF02', 'rDM10', 'rDP03', 
    'rDR04', 'rDS05', 'rDS06', 'rDU11', 'rDX07', 'rDX08', 'rIC05', 'rIC07', 
    'rID13', 'rIH03', 'rIH04', 'rIH06', 'rIH11', 'rIH12', 'rIH14', 'rIH16', 
    'rIL01', 'rIL02', 'rIL08', 'rIL10', 'rIL15', 'rIO09'
    
    """
    IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif')
    METAINFO = {'classes': PLANT_ANOMALY_AREA}

    def __init__(self,
                 data_root: str = '',
                 split: str = '',
                 data_prefix: Union[str, dict] = '',
                 ann_file: str = '',
                 metainfo: Optional[dict] = None,
                 **kwargs):
        kwargs = {'extensions': self.IMG_EXTENSIONS, **kwargs}

        if split:
            splits = ['train', 'val', 'test']
            assert split in splits, \
                f"The split must be one of {splits}, but get '{split}'"

            if split == 'test':
                logger = MMLogger.get_current_instance()
                logger.info(
                    'Since the ImageNet1k test set does not provide label'
                    'annotations, `with_label` is set to False')
                kwargs['with_label'] = False

            data_prefix = split if data_prefix == '' else data_prefix

            if ann_file == '':
                _ann_path = fileio.join_path(data_root, 'meta', f'{split}.txt')
                if fileio.exists(_ann_path):
                    ann_file = fileio.join_path('meta', f'{split}.txt')

        super().__init__(
            data_root=data_root,
            data_prefix=data_prefix,
            ann_file=ann_file,
            metainfo=metainfo,
            **kwargs)

    def extra_repr(self) -> List[str]:
        """The extra repr information of the dataset."""
        body = [
            f'Root of dataset: \t{self.data_root}',
        ]
        return body
    