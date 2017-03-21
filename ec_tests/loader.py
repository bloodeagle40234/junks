from pyeclib.ec_iface import ECDriver
import pickle
from random import shuffle 

if __name__ == '__main__':
    with open('results.pkl', 'rb') as f:
        results_dict = pickle.load(f)

    for key, frags in results_dict.items():
        k, m = key
        driver = ECDriver(ec_type='jerasure_rs_vand', k=k, m=m)
        for num in range(10):
            shuffle(frags)
            assert 'a'*100 == driver.decode(
                frags[:k], force_metadata_checks=True)
        print '%s passed' % str(key)
