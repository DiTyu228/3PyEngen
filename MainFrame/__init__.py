from pydx12 import CreateDXGIFactory2

class Main():
    def __init__(self):
        factory = CreateDXGIFactory2()
        for adapter in factory.EnumAdapters():
            adapter_desc = adapter.GetDesc()
            print('{} ({} MB)'.format(adapter_desc.Description, adapter_desc.DedicatedVideoMemory / 1024 / 1024))