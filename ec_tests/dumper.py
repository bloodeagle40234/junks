from pyeclib.ec_iface import ECDriver
import pickle


if __name__ == '__main__':
    ec_pattern = [(6, 3), (10, 4), (20, 4), (11, 7)]

    results_dict = {}
    for k, m in ec_pattern:
        driver = ECDriver(ec_type='jerasure_rs_vand', k=k, m=m)
        results_dict[(k, m)] = driver.encode('a' * 100)

    with open('results.pkl', 'wb') as f:
        pickle.dump(results_dict, f)
