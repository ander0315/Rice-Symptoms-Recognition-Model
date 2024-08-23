_base_ = [
    '../_base_/models/van/van_large.py',
    '../_base_/schedules/imagenet_bs1024_adamw_swin.py',
    '../_base_/default_runtime.py'
]

model = dict(
    head=dict(num_classes=31)
)


# dataset setting
data_preprocessor = dict(
    num_classes=31,
    mean=[127.5, 127.5, 127.5],
    std=[127.5, 127.5, 127.5],
    # convert image from BGR to RGB
    to_rgb=True,
)

bgr_mean = data_preprocessor['mean'][::-1]
bgr_std = data_preprocessor['std'][::-1]

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='RandomResizedCrop',
        scale=224,
        backend='pillow',
        interpolation='bicubic'),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(
        type='RandAugment',
        policies='timm_increasing',
        num_policies=2,
        total_level=10,
        magnitude_level=9,
        magnitude_std=0.5,
        hparams=dict(
            pad_val=[round(x) for x in bgr_mean], interpolation='bicubic')),
    dict(type='ColorJitter', brightness=0.4, contrast=0.4, saturation=0.4),
    dict(
        type='RandomErasing',
        erase_prob=0.25,
        mode='rand',
        min_area_ratio=0.02,
        max_area_ratio=1 / 3,
        fill_color=bgr_mean,
        fill_std=bgr_std),
    dict(type='NumpyToPIL', to_rgb=True),
    dict(type='PackInputs'),
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='ResizeEdge',
        scale=248,
        edge='short',
        backend='pillow',
        interpolation='bicubic'),
    dict(type='CenterCrop', crop_size=224),
    dict(type='NumpyToPIL', to_rgb=True),
    dict(type='PackInputs'),
]

data_root = r'D:\CHOU\mmpretrain\data\plant_crop_data'

train_dataloader = dict(
    batch_size=64,
    num_workers=5,
    dataset=dict(
        type='CustomDataset',
        data_root=data_root,
        ann_file='',       # 我们假定使用子文件夹格式，因此需要将标注文件置空
        data_prefix='train',    
        pipeline=train_pipeline
    ),
    sampler=dict(type='DefaultSampler', shuffle=True),
)

val_dataloader = dict(
    batch_size=64,
    num_workers=5,
    dataset=dict(
        type='CustomDataset',
        data_root=data_root,
        ann_file='',       # 我们假定使用子文件夹格式，因此需要将标注文件置空
        data_prefix='val',    
        pipeline=test_pipeline
    ),
    sampler=dict(type='DefaultSampler', shuffle=False),
)

test_dataloader = dict(
    batch_size=64,
    num_workers=5,
    dataset=dict(
        type='CustomDataset',
        data_root=data_root,
        ann_file='',       # 我们假定使用子文件夹格式，因此需要将标注文件置空
        data_prefix='test',    
        pipeline=test_pipeline
    ),
    sampler=dict(type='DefaultSampler', shuffle=False),
)

# schedule settings
optim_wrapper = dict(clip_grad=dict(max_norm=5.0))
train_cfg = dict(by_epoch=True, max_epochs=300, val_interval=1)
val_evaluator = [dict(type='Accuracy', topk=(1, 3, 5)),
                 dict(type='SingleLabelMetric', items=['precision', 'recall']),]
# test_dataloader = val_dataloader
test_evaluator = val_evaluator

# configure default hooks
default_hooks = dict(
    # save checkpoint per epoch.
    checkpoint=dict(type='CheckpointHook', interval=1, save_best='auto'),

    # validation results visualization, set True to enable it.
    visualization=dict(type='VisualizationHook', enable=True),
)
visualizer = dict(
    type='UniversalVisualizer',
    vis_backends=[dict(type='LocalVisBackend'), 
                  dict(type='TensorboardVisBackend')],
)