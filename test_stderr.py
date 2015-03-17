import sys
from StringIO import StringIO
from pyeclib.ec_iface import ECDriver

if __name__ == '__main__':
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr
    sio = StringIO()
    sys.stderr = sio
    try:
        ECDriver(k=3, m=1, ec_type='shss')
    except:
        pass
    print 'stderr: %s' % sio.getvalue() 
