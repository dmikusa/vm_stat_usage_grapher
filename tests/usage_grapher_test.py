import dingus
from nose.tools import eq_
from StringIO import StringIO


class TestUsageGrapher(object):
    def test_run_vm_stat(self):
        check_output_dingus = dingus.Dingus()
        check_output_dingus.return_value = "some data here"
        with dingus.patch('subprocess.check_output', check_output_dingus):
            from usage_grapher import run_vm_stat
            output = run_vm_stat()
            eq_(output, "some data here")

    def test_parse_vm_stat_output(self):
        vm_stat_data = open('tests/vm_stat_output.txt').read()
        from usage_grapher import parse_vm_stat_output
        output = parse_vm_stat_output(vm_stat_data)
        eq_(len(output), 23)
        assert 'Swapins' in output.keys()
        assert 'Pages zero filled' in output.keys()
        eq_('1159022', output['Pages purged'])
        eq_('1099822', output['Pages active'])
        eq_('74033590', output['"Translation faults"'])

    def test_store_data(self):
        # get some data
        vm_stat_data = open('tests/vm_stat_output.txt').read()
        from usage_grapher import parse_vm_stat_output
        parsed_data = parse_vm_stat_output(vm_stat_data)
        # create a place for the function to write the data
        buf = StringIO()
        open_dingus = dingus.Dingus()
        open_dingus.return_value.__enter__.return_value = buf
        # run our actual method
        with dingus.patch('__builtin__.open', open_dingus):
            from usage_grapher import persist_vm_stat_data
            persist_vm_stat_data(parsed_data)
        output = buf.getvalue()
        assert output.startswith("74033590,")
        assert output.strip().endswith("384190")

    def test_load_vm_stat_data(self):
        fp = open('tests/usage_grapher.csv', 'rb')
        with dingus.patch('__builtin__.open', lambda *args: fp):
            from usage_grapher import load_vm_stat_data
            vm_stat_data = load_vm_stat_data()
        assert len(vm_stat_data) == 18
        eq_("33403871", vm_stat_data[0]["Pages zero filled"])
        eq_("9004831", vm_stat_data[1]["Pageins"])
