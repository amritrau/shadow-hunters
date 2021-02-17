import pytest
import pandas as pd
import numpy as np


def test_phrasebook():
    # Confirm that there is no more than one translation per phrase
    # per language
    df = pd.read_csv('shadow-hunters/i18n/phrasebook.csv')
    assert len(df) == len(df.drop_duplicates(subset=('phrase_id', 'lang')))

    # Confirm that every language has the same number of translations
    tr_counts = df.groupby(['lang']).count()['phrase_id'].values
    assert np.all(tr_counts == tr_counts[0])
