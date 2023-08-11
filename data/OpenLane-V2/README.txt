put train/val/test datasets here !

└── OpenLane-V2
    ├── train
    |   ├── [segment_id]
    |   |   ├── image                        (Image)
    |   |   |   ├── [camera]
    |   |   |   |   ├── [timestamp].jpg
    |   |   |   |   └── ...
    |   |   |   └── ...
    |   |   ├── sdmap.json                   (SD Map)
    |   |   └── info
    |   |       ├── [timestamp].json         (OpenLane-V2)
    |   |       ├── [timestamp]-ls.json      (Map Element Bucket)
    |   |       └── ...
    |   └── ...
    ├── val
    |   └── ...
    ├── test
    |   └── ...
    ├── data_dict_example.json
    ├── data_dict_subset_A.json
    ├── data_dict_subset_B.json
    ├── openlanev2.md5
    ├── preprocess.py
    └── preprocess-ls.py
