from AnyTest.tests import SublimeFileTestCase


class RspecTestCase(SublimeFileTestCase):
    def test_nearest1(self):
        yield from self.Test('rspec', 'normal_spec.rb', 1)

        self.assertLastCommand('rspec normal_spec.rb:1')

    def test_nearest2(self):
        yield from self.Test('rspec', 'context_spec.rb', 1)
        self.assertLastCommand('rspec context_spec.rb:1')

        yield from self.Test(line=2)
        self.assertLastCommand('rspec context_spec.rb:2')

        yield from self.Test(line=3)
        self.assertLastCommand('rspec context_spec.rb:3')
