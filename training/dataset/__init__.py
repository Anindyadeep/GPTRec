from .movielens import ML100KDataset

DATASETS = {
    ML100KDataset.code(): ML100KDataset,
}


def dataset_factory(args):
    dataset = DATASETS[args.dataset_code]
    return dataset(args)
