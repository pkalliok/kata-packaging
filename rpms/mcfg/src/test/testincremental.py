"""Unit test the incremental task, no other classes used"""

import filecmp
import mock
import os
import sys
import unittest

# we live in subdirectory test, so we need to import the code to be tested
# from the parent directory. I don't like this hack, please suggest something
# better (well, nose does it already, but maybe not everybody uses it)
#
# better suggestion: http://docs.python.org/2/whatsnew/2.5.html
# see section "PEP 328: Absolute and Relative Imports", relative imports
# never touch a working code, so not implemented now
here = os.path.split( __file__ )[0]
if here == '' :
    here = os.getcwd()
above = os.path.split( here )[0]
hackedPath = [ above ]
hackedPath.extend( sys.path )
sys.path = hackedPath

import incremental

class TestIncremental(unittest.TestCase):
    """Unit test the incremental task, no other classes used"""

    def test_construct_and_convert(self):
        """Just construct it and convert to int"""
        inc = incremental.Incremental(7)
        self.assertEqual(7, int(inc))
        os.unlink(incremental.Incremental.get_stat_file_name())

    def test_status_file(self):
        """Test that the last increment is kept correctly
        black box testing as far as file contents is concerned
        """
        filename = incremental.Incremental.get_stat_file_name()
        try:
            os.unlink(filename)
        except OSError:
            pass
        inc = incremental.Incremental(7)
        self.assertEqual(-1, inc.lastincr)
        inc = incremental.Incremental(8)
        self.assertEqual(7, inc.lastincr)
        inc = incremental.Incremental(8)
        # twice the same is not an increment!
        self.assertEqual(-1, inc.lastincr)
        os.unlink(filename)

    def test_is_current(self):
        """Test the is_current method. Depends on correct status file
        operation.
        """
        filename = incremental.Incremental.get_stat_file_name()
        try:
            os.unlink(filename)
        except OSError:
            pass
        inc = incremental.Incremental(7)
        self.assertTrue(inc.is_current(0))
        self.assertTrue(inc.is_current(6))
        self.assertTrue(inc.is_current(7))
        self.assertFalse(inc.is_current(8))
        inc = incremental.Incremental(10)
        self.assertFalse(inc.is_current(7))
        self.assertTrue(inc.is_current(8))
        self.assertTrue(inc.is_current(9))
        self.assertTrue(inc.is_current(10))
        self.assertFalse(inc.is_current(11))

        # also test a non-integer
        action = mock.Mock()
        action.__int__ = mock.Mock()         # magic method needs to be
                                             # explicitly assigned
        action.__int__.return_value = 10
        self.assertTrue(inc.is_current(action))
        action.__int__.return_value = 11
        self.assertFalse(inc.is_current(action))
        os.unlink(filename)

    def test_copy_success(self):
        """Test successful copying of the status file"""
        new = 'foonew'   # these names should not match real user-specific
                         # ones, so all files should be owned by the user
                         # running the test. We ignore all issues caused
                         # by wrong ownership (like unlink failing because
                         # file is owned by somebody else)
        old = 'fooold'
        old_filename = incremental.Incremental.get_stat_file_name(old)
        try:
            os.unlink(old_filename)
        except OSError:
            pass
        new_filename = incremental.Incremental.get_stat_file_name(new)
        try:
            os.unlink(new_filename)
        except OSError:
            pass
        os.system("dd if=/dev/urandom of={0} count=1".format( old_filename))
        incremental.Incremental.copy_stat_file(old, new)
        result = filecmp.cmp(old_filename, new_filename)
        if result:
            os.unlink(old_filename)
            os.unlink(new_filename)
        else:
            print >> sys.stderr, "files did not match: {0} and {1}".format(
                                  old_filename, new_filename)
        self.assertTrue(result)

    def test_copy_failure(self):
        """Test failure handling while copying the status file"""
        old = "foodoesnotexist"
        new = "foobardoesnotexist"
        self.assertRaises(IOError, incremental.Incremental.copy_stat_file,
                                  old, new)
        # in Python 2.7 we could have used assertRaises as context manager,
        # in the first place, but we need to support Python 2.6
        # (of course this could be coded differently using try, but the
        # assertRaises conveys the idea what we are doing)
        try:
            incremental.Incremental.copy_stat_file(old, new)
        except IOError as exc:
            cmd = "cp {0} {1}".format(
                    incremental.Incremental.get_stat_file_name(old),
                    incremental.Incremental.get_stat_file_name(new))
            msg = "Problem executing {0}".format(cmd)
            self.assertEqual(msg, str(exc))



if __name__ == '__main__':
    unittest.main()
