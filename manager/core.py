def execute_from_command_line(argv):
    try:
        _address = {'host': '127.0.0.1', 'port': '8000'}
        if argv.__len__() > 1:
            arg_address = argv[1].split(':')
            _address['host'] = arg_address[0]
            _address['port'] = arg_address[1]
    except Exception as e:
        raise ValueError('wrong address')
    return _address
