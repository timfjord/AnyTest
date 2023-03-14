from AnyTest.tests import SublimeProjectTestCase


class MinitestRakeTestCase(SublimeProjectTestCase):
    folder = ("minitest", "rake")

    def test_line_unit_syntax(self):
        yield from self._testFile("classic_unit_test.rb", 3)
        self.assertLastCommand(
            'rake test TEST="classic_unit_test.rb" TESTOPTS="--name=/Math/"'
        )

        self._testLine(4)
        self.assertLastCommand(
            'rake test TEST="classic_unit_test.rb" TESTOPTS="--name=/Math::TestNumbers/"'
        )

        self._testLine(6)
        self.assertLastCommand(
            (
                'rake test TEST="classic_unit_test.rb" '
                'TESTOPTS="--name=/Math::TestNumbers#test_method\\$/"'
            )
        )

        yield from self._testFile("test_classic.rb", 3)
        self.assertLastCommand(
            'rake test TEST="test_classic.rb" TESTOPTS="--name=/Math/"'
        )

        self._testLine(4)
        self.assertLastCommand(
            'rake test TEST="test_classic.rb" TESTOPTS="--name=/Math::TestOperators/"'
        )

        self._testLine(6)
        self.assertLastCommand(
            (
                'rake test TEST="test_classic.rb" '
                'TESTOPTS="--name=/Math::TestOperators#test_addition\\$/"'
            )
        )

        yield from self._testFile("rails_unit_test.rb", 11)
        self.assertLastCommand(
            (
                'rake test TEST="rails_unit_test.rb" '
                'TESTOPTS="--name=/MathTest#test_double_quotes\\$/"'
            )
        )

        self._testLine(15)
        self.assertLastCommand(
            (
                'rake test TEST="rails_unit_test.rb" '
                'TESTOPTS="--name=/MathTest#test_single_quotes\\$/"'
            )
        )

        self._testLine(19)
        self.assertLastCommand(
            (
                'rake test TEST="rails_unit_test.rb" '
                'TESTOPTS="--name=/MathTest#test_single_quote_\'_inside\\$/"'
            )
        )

        self._testLine(23)
        self.assertLastCommand(
            (
                'rake test TEST="rails_unit_test.rb" '
                'TESTOPTS="--name=/MathTest#test_double_quote_\\"_inside\\$/"'
            )
        )

        self._testLine(27)
        self.assertLastCommand(
            (
                'rake test TEST="rails_unit_test.rb" '
                'TESTOPTS="--name=/MathTest#test_pending_test\\$/"'
            )
        )

        self._testLine(29)
        self.assertLastCommand(
            'rake test TEST="rails_unit_test.rb" TESTOPTS="--name=/MathTest#test_parentheses\\$/"'
        )

    def test_line_spec_syntax(self):
        yield from self._testFile("classic_spec_test.rb", 6)
        self.assertLastCommand(
            'rake test TEST="classic_spec_test.rb" TESTOPTS="--name=/Math/"'
        )

        self._testLine(7)
        self.assertLastCommand(
            'rake test TEST="classic_spec_test.rb" TESTOPTS="--name=/Math::TestNumbers/"'
        )

        self._testLine(8)
        self.assertLastCommand(
            (
                'rake test TEST="classic_spec_test.rb" '
                'TESTOPTS="--name=/Math::TestNumbers#test_\\d+_has double quotes\\$/"'
            )
        )

        self._testLine(12)
        self.assertLastCommand(
            (
                'rake test TEST="classic_spec_test.rb" '
                'TESTOPTS="--name=/Math::TestNumbers#test_\\d+_has single quotes\\$/"'
            )
        )

        self._testLine(16)
        self.assertLastCommand(
            (
                'rake test TEST="classic_spec_test.rb" '
                'TESTOPTS="--name=/Math::TestNumbers#test_\\d+_contains a \'\\$/"'
            )
        )

        self._testLine(20)
        self.assertLastCommand(
            (
                'rake test TEST="classic_spec_test.rb" '
                'TESTOPTS="--name=/Math::TestNumbers#test_\\d+_contains a \\"\\$/"'
            )
        )

        self._testLine(24)
        self.assertLastCommand(
            (
                'rake test TEST="classic_spec_test.rb" '
                'TESTOPTS="--name=/Math::TestNumbers#test_\\d+_contains \\`backticks\\`\\$/"'
            )
        )

        self._testLine(28)
        self.assertLastCommand(
            (
                'rake test TEST="classic_spec_test.rb" '
                'TESTOPTS="--name=/Math::TestNumbers#test_\\d+_is pending\\$/"'
            )
        )

        self._testLine(30)
        self.assertLastCommand(
            (
                'rake test TEST="classic_spec_test.rb" '
                'TESTOPTS="--name=/Math::TestNumbers#test_\\d+_has parentheses\\$/"'
            )
        )

        self._testLine(32)
        self.assertLastCommand(
            (
                'rake test TEST="classic_spec_test.rb" '
                'TESTOPTS="--name=/Math::TestNumbers::Parentheses/"'
            )
        )

        yield from self._testFile("explicit_spec_test.rb", 4)
        self.assertLastCommand(
            'rake test TEST="explicit_spec_test.rb" TESTOPTS="--name=/MathSpec/"'
        )

        self._testLine(5)
        self.assertLastCommand(
            'rake test TEST="explicit_spec_test.rb" TESTOPTS="--name=/MathSpec#test_\\d+_is\\$/"'
        )

    def test_line_no_nearest(self):
        yield from self._testFile("classic_unit_test.rb", 1)
        self.assertLastCommand('rake test TEST="classic_unit_test.rb"')

    def test_file(self):
        yield from self._testFile("classic_unit_test.rb")
        self.assertLastCommand('rake test TEST="classic_unit_test.rb"')

    def test_suite(self):
        yield from self._testSuite("classic_unit_test.rb")
        self.assertLastCommand("find test -name *_test.rb -exec rake test {} +")

    def test_suite_with_custom_folder_and_pattern(self):
        self.setSettings(
            {
                "ruby.minitest.test_folder": "my_test",
                "ruby.minitest.file_pattern": "*_my_test.rb",
            }
        )

        yield from self._testSuite("classic_unit_test.rb")
        self.assertLastCommand("find my_test -name *_my_test.rb -exec rake test {} +")
