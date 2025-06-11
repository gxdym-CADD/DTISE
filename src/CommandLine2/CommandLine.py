# llvm/Support/CommandLine.py - Command line handler -*- Python -*-

from typing import Callable, List, Optional

def parse_command_line_options(argc: int, argv: List[str], overview: Optional[str] = None, read_response_files: bool = False) -> None:
    pass

def parse_environment_options(prog_name: str, env_var: str, overview: Optional[str] = None, read_response_files: bool = False) -> None:
    pass

def set_version_printer(func: Callable[[], None]) -> None:
    pass

def mark_options_changed() -> None:
    pass
from typing import Callable, List, Optional

def parse_command_line_options(argc: int, argv: List[str], overview: Optional[str] = None, read_response_files: bool = False) -> None:
    pass

def parse_environment_options(prog_name: str, env_var: str, overview: Optional[str] = None, read_response_files: bool = False) -> None:
    pass

def set_version_printer(func: Callable[[], None]) -> None:
    pass

def mark_options_changed() -> None:
    pass

# SetVersionPrinter - Override the default (LLVM specific) version printer
#                     used to print out the version when --version is given
#                     on the command line. This allows other systems using the
#                     CommandLine utilities to print their own version string.
def set_version_printer(func: Callable[[], None]) -> None:
    pass

# MarkOptionsChanged - Internal helper function.
def mark_options_changed() -> None:
    pass

# Flags permitted to be passed to command line arguments
#

class NumOccurrencesFlag:
    Optional = 0x01      # Zero or One occurrence
    ZeroOrMore = 0x02    # Zero or more occurrences allowed
    Required = 0x03      # One occurrence required
    OneOrMore = 0x04     # One or more occurrences required

    ConsumeAfter = 0x05  # Indicates that this option is fed anything that follows the
                        # last positional argument required by the application (it is an error if
                        # there are zero positional arguments, and a ConsumeAfter option is used).
                        # Thus, for example, all arguments to LLI are processed until a filename is
                        # found.  Once a filename is found, all of the succeeding arguments are
                        # passed, unprocessed, to the ConsumeAfter option.

    OccurrencesMask = 0x07

class ValueExpected:
    ValueOptional = 0x08   # The value can appear... or not
    ValueRequired = 0x10   # The value is required to appear!
    ValueDisallowed = 0x18 # A value may not be specified (for flags)
    ValueMask = 0x18

class OptionHidden:
    NotHidden = 0x20     # Option included in --help & --help-hidden
    Hidden = 0x40        # -help doesn't, but --help-hidden does
    ReallyHidden = 0x60   # Neither --help nor --help-hidden show this arg
    HiddenMask = 0x60

class FormattingFlags:
    NormalFormatting = 0x000     # Nothing special
    Positional = 0x080          # Is a positional argument, no '-' required
    Prefix = 0x100              # Can this option directly prefix its value?
    Grouping = 0x180            # Can this option group with other options?
    FormattingMask = 0x180      # Union of the above flags.

class MiscFlags:
    CommaSeparated = 0x200     # Should this cl::list split between commas?
    PositionalEatsArgs = 0x400 # Should this positional cl::list eat -args?
    Sink = 0x800               # Should this cl::list eat all unknown options?
    MiscMask = 0xE00           # Union of the above flags.

# Option Base class
#
class alias:
    pass

class Option:
    def __init__(self):
        pass

    def handle_occurrence(self, pos: int, arg_name: str, arg: str) -> bool:
        raise NotImplementedError("Subclasses should implement this method")

    def get_value_expected_flag_default(self) -> ValueExpected:
        return ValueExpected.ValueOptional

    def anchor(self):
        pass
from enum import Enum

class ValueExpected(Enum):
    ValueOptional = 0
    # Add other values as needed

class NumOccurrencesFlag(Enum):
    OccurrencesNone = 1
    OccurrencesOne = 2
    OccurrencesZeroOrMore = 3
    OccurrencesOneOrMore = 4

class OptionHidden(Enum):
    HiddenNone = 0
    HiddenInternal = 1

class FormattingFlags(Enum):
    NormalFormatting = 0
    # Add other values as needed

class MiscFlags(Enum):
    MiscMask = 0xE00

OccurrencesMask = 0xF00
ValueMask = 0x0F0
HiddenMask = 0x00F
FormattingMask = 0x0F00

# Option Base class
#
class alias:
    pass

class Option:
    def __init__(self, default_flags):
        self.NumOccurrences = 0
        self.Flags = default_flags | FormattingFlags.NormalFormatting.value
        self.Position = 0
        self.AdditionalVals = 0
        self.NextRegistered = None
        self.ArgStr = ""
        self.HelpStr = ""
        self.ValueStr = ""

    def handle_occurrence(self, pos: int, arg_name: str, arg: str) -> bool:
        raise NotImplementedError("Subclasses should implement this method")

    def get_value_expected_flag_default(self) -> ValueExpected:
        return ValueExpected.ValueOptional

    def anchor(self):
        pass

    def get_num_occurrences_flag(self) -> NumOccurrencesFlag:
        return NumOccurrencesFlag(self.Flags & OccurrencesMask)

    def get_value_expected_flag(self) -> ValueExpected:
        ve = self.Flags & ValueMask
        return ValueExpected(ve) if ve else self.get_value_expected_flag_default()

    def get_option_hidden_flag(self) -> OptionHidden:
        return OptionHidden(self.Flags & HiddenMask)

    def get_formatting_flag(self) -> FormattingFlags:
        return FormattingFlags(self.Flags & FormattingMask)

    def get_misc_flags(self) -> int:
        return self.Flags & MiscMask

    def get_position(self) -> int:
        return self.Position

    def get_num_additional_vals(self) -> int:
        return self.AdditionalVals

    # hasArgStr - Return true if the argstr != ""
    def has_arg_str(self) -> bool:
        return self.ArgStr[0] != 0

    # Accessor functions set by OptionModifiers
    #
    def set_arg_str(self, s: str):
        self.ArgStr = s

    def set_description(self, s: str):
        self.HelpStr = s

    def set_value_str(self, s: str):
        self.ValueStr = s

    def set_flag(self, flag: int, flag_mask: int):
        self.Flags &= ~flag_mask
        self.Flags |= flag

    def set_num_occurrences_flag(self, val: NumOccurrencesFlag):
        self.set_flag(val.value, OccurrencesMask)

    def set_value_expected_flag(self, val: ValueExpected):
        self.set_flag(val.value, ValueMask)

    def set_hidden_flag(self, val: OptionHidden):
        self.set_flag(val.value, HiddenMask)

    def set_formatting_flag(self, v: FormattingFlags):
        self.set_flag(v.value, FormattingMask)

    def set_misc_flag(self, m: MiscFlags):
        self.set_flag(m.value, m.value)

    def set_position(self, pos: int):
        self.Position = pos

    def set_num_additional_vals(self, n: int):
        self.AdditionalVals = n

    # addArgument - Register this argument with the commandline system.
    #
    def add_argument(self):
        pass

    def get_next_registered_option(self) -> 'Option':
        return self.NextRegistered

    # Return the width of the option tag for printing...
    def get_option_width(self) -> int:
        raise NotImplementedError("Subclasses should implement this method")

    # printOptionInfo - Print out information about this option.  The
    # always returns true.
    def add_occurrence(self, pos: int, arg_name: str, value: str, multi_arg: bool = False) -> bool:
        raise NotImplementedError("Subclasses should implement this method")

    # Prints option name followed by message.  Always returns true.
    def error(self, message: str, arg_name: str = "") -> bool:
        raise NotImplementedError("Subclasses should implement this method")

    def get_num_occurrences(self) -> int:
        return self.NumOccurrences

    def __del__(self):
        pass

# Command line option modifiers that can be used to modify the behavior of
# command line option parsers...
#

# desc - Modifier to set the description shown in the --help output...
class desc:
    def __init__(self, str: str):
        self.Desc = str

    def apply(self, o: Option) -> None:
        o.set_description(self.Desc)
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

class Option(ABC):
    def __init__(self, desc: str = "", value_desc: str = "", initial_value: Any = None, location: Any = None):
        self.description = desc
        self.value_description = value_desc
        self.initial_value = initial_value
        self.location = location
        self.num_occurrences = 0

    @abstractmethod
    def set_description(self, desc: str) -> None:
        pass

    @abstractmethod
    def set_value_str(self, value_desc: str) -> None:
        pass

    @abstractmethod
    def set_initial_value(self, initial_value: Any) -> None:
        pass

    @abstractmethod
    def set_location(self, location: Any) -> None:
        pass

    def get_num_occurrences(self) -> int:
        return self.num_occurrences

    def __del__(self):
        pass

class desc:
    def __init__(self, str_desc: str):
        self.Desc = str_desc

    def apply(self, o: Option) -> None:
        o.set_description(self.Desc)

class value_desc:
    def __init__(self, str_value_desc: str):
        self.Desc = str_value_desc

    def apply(self, o: Option) -> None:
        o.set_value_str(self.Desc)

class initializer:
    def __init__(self, init_val: Any):
        self.Init = init_val

    def apply(self, o: Option) -> None:
        o.set_initial_value(self.Init)

def init(val: Any) -> initializer:
    return initializer(val)

class LocationClass:
    def __init__(self, loc: Any):
        self.Loc = loc

    def apply(self, o: Option) -> None:
        o.set_location(self.Loc)

def location(loc: Any) -> LocationClass:
    return LocationClass(loc)

class ValuesClass:
    def __init__(self, enum_name: str, val: Any, desc: str, *value_args: Tuple[str, int, str]):
        self.Values = [(enum_name, (val, desc))]
        for arg in value_args:
            self.Values.append(arg)

    def apply(self, o: Option) -> None:
        for enum_name, (enum_val, enum_desc) in self.Values:
            o.get_parser().add_literal_option(enum_name, enum_val, enum_desc)

def values(arg: str, val: Any, desc: str, *value_args: Tuple[str, int, str]) -> ValuesClass:
    return ValuesClass(arg, val, desc, *value_args)
class ValuesClass:
    def __init__(self, arg: str, val: Any, desc: str, *value_args: Tuple[str, int, str]):
        self.Values = [(arg, (val, desc))]
        for arg in value_args:
            self.Values.append(arg)

    def apply(self, o: Option) -> None:
        for enum_name, (enum_val, enum_desc) in self.Values:
            o.get_parser().add_literal_option(enum_name, enum_val, enum_desc)

def values(arg: str, val: Any, desc: str, *value_args: Tuple[str, int, str]) -> ValuesClass:
    return ValuesClass(arg, val, desc, *value_args)

# Template class in C++ is converted to a generic function in Python
def end_with_null_values(arg: str, val: Any, desc: str, **kwargs) -> ValuesClass:
    values = [(arg, (val, desc))]
    for key, value in kwargs.items():
        values.append((key, value))
    return ValuesClass(*values)

class Option:
    def __init__(self, has_arg_str: bool):
        self.has_arg_str = has_arg_str

    def get_parser(self) -> 'Parser':
        pass

    def error(self, message: str) -> None:
        print(f"Error: {message}")

    def hasArgStr(self) -> bool:
        return self.has_arg_str

class Parser:
    def add_literal_option(self, enum_name: str, enum_val: Any, enum_desc: str):
        pass

class GenericParserBase:
    def __init__(self):
        self.has_arg_str = False

    def get_num_options(self) -> int:
        raise NotImplementedError

    def get_option(self, n: int) -> str:
        raise NotImplementedError

    def get_description(self, n: int) -> str:
        raise NotImplementedError

    def get_option_width(self, o: Option) -> int:
        pass

    def print_option_info(self, o: Option, global_width: int) -> None:
        pass

    def initialize(self, o: Option) -> None:
        self.has_arg_str = o.hasArgStr()

    def get_extra_option_names(self, option_names: List[str]) -> None:
        if not self.has_arg_str:
            for i in range(self.get_num_options()):
                option_names.append(self.get_option(i))

    def get_value_expected_flag_default(self) -> str:
        if self.has_arg_str:
            return "ValueRequired"
        else:
            return "ValueDisallowed"

    def find_option(self, name: str) -> int:
        for i in range(self.get_num_options()):
            if self.get_option(i) == name:
                return i
        return self.get_num_options()

class ParserTemplate(GenericParserBase):
    def __init__(self, values: List[Tuple[str, Tuple[Any, str]]]):
        super().__init__()
        self.values = values

    def get_num_options(self) -> int:
        return len(self.values)

    def get_option(self, n: int) -> str:
        return self.values[n][0]

    def get_description(self, n: int) -> str:
        return self.values[n][1][1]

    def parse(self, o: Option, arg_name: str, arg: str, v: Any) -> bool:
        arg_val = arg if self.has_arg_str else arg_name
        for i in range(len(self.values)):
            if self.values[i][0] == arg_val:
                v[0] = self.values[i][1][0]
                return False
        return o.error(f"Cannot find option named '{arg_val}'!")
class Option:
    def __init__(self, arg_str):
        self.arg_str = arg_str

    def error(self, message):
        print(f"Error: {message}")
        return True

class ParserBase:
    def get_value_expected_flag_default(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_extra_option_names(self):
        return []

    def initialize(self, option):
        pass

    def get_option_width(self, option):
        raise NotImplementedError("Subclasses must implement this method")

    def print_option_info(self, option, global_width):
        raise NotImplementedError("Subclasses must implement this method")

    def get_value_name(self):
        return "value"

    def anchor(self):
        pass

class BasicParser(ParserBase):
    def __init__(self, data_type):
        self.data_type = data_type

    def parse(self, option, arg_name, arg, v):
        raise NotImplementedError("Subclasses must implement this method")

class BoolParser(BasicParser):
    def __init__(self):
        super().__init__(bool)
        self.arg_str = None

    def parse(self, option, arg_name, arg, val):
        self.arg_str = option.arg_str
        if arg in ('true', '1'):
            val[0] = True
            return False
        elif arg in ('false', '0'):
            val[0] = False
            return False
        else:
            return option.error(f"Invalid value for boolean option '{arg}'!")

    def get_value_expected_flag_default(self):
        return "ValueOptional"

    def get_value_name(self):
        return None

class BoolOrDefaultParser(BasicParser):
    def __init__(self):
        super().__init__("boolOrDefault")

    def parse(self, option, arg_name, arg, val):
        if arg in ('true', '1'):
            val[0] = "BOU_TRUE"
            return False
        elif arg in ('false', '0'):
            val[0] = "BOU_FALSE"
            return False
        else:
            val[0] = "BOU_UNSET"
            return False

    def get_value_expected_flag_default(self):
        return "ValueOptional"

    def get_value_name(self):
        return None

class IntParser(BasicParser):
    def __init__(self):
        super().__init__(int)

    def parse(self, option, arg_name, arg, val):
        try:
            val[0] = int(arg)
            return False
        except ValueError:
            return option.error(f"Invalid value for integer option '{arg}'!")

    def get_value_name(self):
        return "int"

class UnsignedParser(BasicParser):
    def __init__(self):
        super().__init__(unsigned)

    def parse(self, option, arg_name, arg, val):
        try:
            val[0] = int(arg)
            if val[0] < 0:
                raise ValueError
            return False
        except ValueError:
            return option.error(f"Invalid value for unsigned integer option '{arg}'!")

    def get_value_name(self):
        return "uint"
class UnsignedParser(BasicParser):
    def __init__(self):
        super().__init__(unsigned)

    def parse(self, option, arg_name, arg, val):
        try:
            val[0] = int(arg)
            if val[0] < 0:
                raise ValueError
            return False
        except ValueError:
            return option.error(f"Invalid value for unsigned integer option '{arg}'!")

    def get_value_name(self):
        return "uint"

class DoubleParser(BasicParser):
    def __init__(self):
        super().__init__(double)

    def parse(self, option, arg_name, arg, val):
        try:
            val[0] = float(arg)
            return False
        except ValueError:
            return option.error(f"Invalid value for double option '{arg}'!")

    def get_value_name(self):
        return "number"

class FloatParser(BasicParser):
    def __init__(self):
        super().__init__(float)

    def parse(self, option, arg_name, arg, val):
        try:
            val[0] = float(arg)
            return False
        except ValueError:
            return option.error(f"Invalid value for float option '{arg}'!")

    def get_value_name(self):
        return "number"

class StringParser(BasicParser):
    def __init__(self):
        super().__init__(str)

    def parse(self, option, arg_name, arg, val):
        val[0] = arg
        return False

    def get_value_name(self):
        return "string"

class CharParser(BasicParser):
    def __init__(self):
        super().__init__(char)

    def parse(self, option, arg_name, arg, val):
        if len(arg) != 1:
            return option.error(f"Invalid value for char option '{arg}'!")
        val[0] = arg[0]
        return False

    def get_value_name(self):
        return "char"

# Applicator class to handle special cases
class Applicator:
    @staticmethod
    def opt(mod, opt):
        mod.apply(opt)

class StringApplicator(Applicator):
    @staticmethod
    def opt(str_val, opt):
        opt.set_arg_str(str_val)

class NumOccurrencesFlagApplicator(Applicator):
    @staticmethod
    def opt(no_flag, opt):
        opt.set_num_occurrences_flag(no_flag)

class ValueExpectedApplicator(Applicator):
    @staticmethod
    def opt(ve_flag, opt):
        opt.set_value_expected_flag(ve_flag)

class OptionHiddenApplicator(Applicator):
    @staticmethod
    def opt(oh_flag, opt):
        opt.set_hidden_flag(oh_flag)

class FormattingFlagsApplicator(Applicator):
    @staticmethod
    def opt(ff_flag, opt):
        opt.set_formatting_flag(ff_flag)

class MiscFlagsApplicator(Applicator):
    @staticmethod
    def opt(mf_flag, opt):
        opt.set_misc_flag(mf_flag)
class Applicator:
    @staticmethod
    def opt(flag, opt):
        raise NotImplementedError("Subclasses must implement this method")

class ueExpectedApplicator(Applicator):
    @staticmethod
    def opt(ve_flag, opt):
        opt.set_value_expected_flag(ve_flag)

class OptionHiddenApplicator(Applicator):
    @staticmethod
    def opt(oh_flag, opt):
        opt.set_hidden_flag(oh_flag)

class FormattingFlagsApplicator(Applicator):
    @staticmethod
    def opt(ff_flag, opt):
        opt.set_formatting_flag(ff_flag)

class MiscFlagsApplicator(Applicator):
    @staticmethod
    def opt(mf_flag, opt):
        opt.set_misc_flag(mf_flag)

def apply(M, O):
    applicator = {
        OptionHidden: lambda OH, O: O.set_hidden_flag(OH),
        FormattingFlags: lambda FF, O: O.set_formatting_flag(FF),
        MiscFlags: lambda MF, O: O.set_misc_flag(MF)
    }.get(type(M), lambda _, __: None)(M, O)

class opt_storage:
    def __init__(self, external_storage=False, is_class=False):
        self.Location = None
        self.external_storage = external_storage
        self.is_class = is_class

    def check(self):
        assert self.Location is not None, "cl::location(...) not specified for a command line option with external storage, or cl::init specified before cl::location()!!"

    def set_location(self, O, L):
        if self.Location:
            raise ValueError("cl::location(x) specified more than once!")
        self.Location = L
        return False

    def set_value(self, V):
        self.check()
        self.Location = V

    def get_value(self):
        self.check()
        return self.Location

    def __call__(self):
        return self.get_value()

class opt_storage_class(opt_storage):
    def set_value(self, V):
        super().set_value(V)

    def get_value(self):
        return self

class opt_storage_container(opt_storage):
    def __init__(self, external_storage=False, is_class=False):
        super().__init__(external_storage, is_class)
        self.Value = None

    def set_value(self, V):
        self.Value = V

    def get_value(self):
        return self.Value

    def __call__(self):
        return self.get_value()

    def __getattr__(self, name):
        if self.is_pointer() and name == '__getattr__':
            return getattr(self.Value, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

class opt(Option, opt_storage):
    def __init__(self, external_storage=False, parser_class=None):
        super().__init__()
        self.Parser = parser_class()
        self.done()

    def handle_occurrence(self, pos, arg_name, arg):
        val = self.Parser.parse(arg_name, arg)
        if not val:
            return True
        self.set_value(val)
        self.set_position(pos)
        return False

    def get_value_expected_flag_default(self):
        return self.Parser.get_value_expected_flag_default()

    def get_extra_option_names(self, option_names):
        return self.Parser.get_extra_option_names(option_names)

    def get_option_width(self):
        return self.Parser.get_option_width(self)

    def print_option_info(self, global_width):
        self.Parser.print_option_info(self, global_width)

    def done(self):
        self.add_argument()
        self.Parser.initialize(self)

    def set_initial_value(self, V):
        self.set_value(V)

    def get_parser(self):
        return self.Parser

    def __set__(self, instance, value):
        self.set_value(value)
        return self.get_value()

# Example usage
class Option:
    def set_hidden_flag(self, flag):
        pass

    def set_formatting_flag(self, flag):
        pass

    def set_misc_flag(self, flag):
        pass

    def set_position(self, pos):
        pass

    def add_argument(self):
        pass

class Parser:
    def parse(self, arg_name, arg):
        return True

    def get_value_expected_flag_default(self):
        return "default"

    def get_extra_option_names(self, option_names):
        pass

    def get_option_width(self, option):
        return 10

    def print_option_info(self, option, global_width):
        pass

    def initialize(self, option):
        pass
class ParserClass:
    def __init__(self):
        self.Parser = Parser()

    def setInitialValue(self, V):
        self.setValue(V)

    def getParser(self):
        return self.Parser

    def setValue(self, Val):
        # Placeholder for setValue method
        pass

    def getValue(self):
        # Placeholder for getValue method
        return None

    def apply(self, modifier, option):
        # Placeholder for apply method
        pass

    def done(self):
        # Placeholder for done method
        pass

class Parser:
    def parse(self, arg_name, arg):
        return True

    def get_value_expected_flag_default(self):
        return "default"

    def get_extra_option_names(self, option_names):
        pass

    def get_option_width(self, option):
        return 10

    def print_option_info(self, option, global_width):
        pass

    def initialize(self, option):
        pass

class opt:
    Optional = 1
    NotHidden = 2

    def __init__(self, *modifiers):
        self.Option = self.Optional | self.NotHidden
        for modifier in modifiers:
            self.apply(modifier, self)
        self.done()

    def apply(self, modifier, option):
        # Placeholder for apply method
        pass

    def done(self):
        # Placeholder for done method
        pass

class list_storage:
    def __init__(self):
        self.Location = None

    def setLocation(self, O, L):
        if self.Location:
            return O.error("cl::location(x) specified more than once!")
        self.Location = L
        return False

    def addValue(self, V):
        assert self.Location is not None and "cl::location(...) not specified for a command line option with external storage!"
        self.Location.append(V)

class list_storage_bool(list):
    def addValue(self, V):
        self.append(V)
from typing import List, TypeVar, Generic, Union

T = TypeVar('T')

class list_storage(Generic[T]):
    def addValue(self, V: T):
        self.append(V)

class list_storage_bool(list):
    def addValue(self, V: bool):
        self.append(V)

class Option:
    ZeroOrMore = 1
    NotHidden = 2

    def __init__(self, flags: int):
        self.flags = flags

    def setNumAdditionalVals(self, n: int):
        pass

class parser(Generic[T]):
    @staticmethod
    def parse(option: 'Option', ArgName: str, Arg: str, Val) -> bool:
        # Placeholder for actual parsing logic
        return False

    def getValueExpectedFlagDefault(self) -> int:
        return 0

    def getExtraOptionNames(self, OptionNames: List[str]):
        pass

    def initialize(self, option: 'Option'):
        pass

    def printOptionInfo(self, option: 'Option', GlobalWidth: int):
        pass

    def getOptionWidth(self, option: 'Option') -> int:
        return 0

class list(Generic[T], Option, list_storage[T]):
    Positions: List[int]

    def __init__(self, *args):
        self.Positions = []
        self.Parser = ParserClass()
        super().__init__(Option.ZeroOrMore | Option.NotHidden)
        for arg in args:
            self.apply(arg, self)
        self.done()

    def apply(self, M0t, option: 'Option'):
        # Placeholder for actual application logic
        pass

    def done(self):
        self.addArgument()
        self.Parser.initialize(self)

    def getParser(self) -> ParserClass:
        return self.Parser

    def getPosition(self, optnum: int) -> int:
        assert optnum < len(self) and "Invalid option index"
        return self.Positions[optnum]

    def handleOccurrence(self, pos: int, ArgName: str, Arg: str) -> bool:
        Val = ParserClass.parser_data_type()
        if self.Parser.parse(self, ArgName, Arg, Val):
            return True  # Parse Error!
        self.addValue(Val)
        self.Positions.append(pos)
        return False

    def addArgument(self):
        pass

class multi_val:
    def __init__(self, N: int):
        self.AdditionalVals = N
class bits_storage:
    def __init__(self):
        self.Location = None

    def setLocation(self, O, L):
        if self.Location is not None:
            return True  # Error: cl::location(x) specified more than once!
        self.Location = L
        return False

    def addValue(self, V):
        assert self.Location is not None, "cl::location(...) not specified for a command line option with external storage!"
        self.Location |= (1 << V)

    def getBits(self):
        return self.Location

    def isSet(self, V):
        return (self.Location & (1 << V)) != 0

class bits_storage_bool:
    def __init__(self):
        self.Bits = 0

    def addValue(self, V):
        self.Bits |= (1 << V)

    def getBits(self):
        return self.Bits

    def isSet(self, V):
        return (self.Bits & (1 << V)) != 0

class bits:
    def __init__(self, *modifiers):
        self.Positions = []
        self.Parser = ParserClass()
        self.Option(ZeroOrMore | NotHidden)
        for modifier in modifiers:
            apply(modifier, self)
        self.done()

    def done(self):
        addArgument()
        self.Parser.initialize(self)

    def handleOccurrence(self, pos, ArgName, Arg):
        Val = ParserClass.parser_data_type()
        if self.Parser.parse(self, ArgName, Arg, Val):
            return True  # Parse Error!
        self.addValue(Val)
        setPosition(pos)
        self.Positions.append(pos)
        return False

    def getPosition(self, optnum):
        assert optnum < len(self) and "Invalid option index"
        return self.Positions[optnum]

    def getParser(self):
        return self.Parser

# Placeholder for ParserClass and other dependencies
class ParserClass:
    @staticmethod
    def parser_data_type():
        pass

    def parse(self, *args):
        pass

    def getValueExpectedFlagDefault(self):
        pass

    def getExtraOptionNames(self, OptionNames):
        pass

    def initialize(self, option):
        pass

def apply(modifier, obj):
    modifier.apply(obj)

ZeroOrMore = 1
NotHidden = 2
class Option:
    def __init__(self):
        self.Option = 0

    def handleOccurrence(self, pos, ArgName, Arg):
        raise NotImplementedError("Subclasses must implement this method")

    def getOptionWidth(self):
        raise NotImplementedError("Subclasses must implement this method")

    def printOptionInfo(self, GlobalWidth):
        raise NotImplementedError("Subclasses must implement this method")

    def addArgument(self):
        pass

    def hasArgStr(self):
        raise NotImplementedError("Subclasses must implement this method")

    def error(self, message):
        raise ValueError(message)

class bits(Option):
    def __init__(self, *modifiers):
        super().__init__()
        self.Option = ZeroOrMore | NotHidden
        for modifier in modifiers:
            apply(modifier, self)
        self.done()

    def done(self):
        pass

ZeroOrMore = 1
NotHidden = 2

def apply(modifier, obj):
    modifier.apply(obj)

class alias(Option):
    def __init__(self, *modifiers):
        super().__init__()
        self.Option = Optional | Hidden
        self.AliasFor = None
        for modifier in modifiers:
            apply(modifier, self)
        self.done()

    def done(self):
        if not self.hasArgStr():
            self.error("cl::alias must have argument name specified!")
        if self.AliasFor is None:
            self.error("cl::alias must have an cl::aliasopt(option) specified!")
        self.addArgument()

    def setAliasFor(self, O):
        if self.AliasFor:
            self.error("cl::alias must only have one cl::aliasopt(...) specified!")
        self.AliasFor = O

class aliasopt:
    def __init__(self, Opt):
        self.Opt = Opt

    def apply(self, A):
        A.setAliasFor(self.Opt)

class extrahelp:
    def __init__(self, help):
        self.morehelp = help

def PrintVersionMessage():
    pass
class extrahelp:
    def __init__(self, help):
        self.morehelp = help

def PrintVersionMessage():
    pass

def PrintHelpMessage():
    # This function just prints the help message, exactly the same way as if the
    # --help option had been given on the command line.
    # NOTE: THIS FUNCTION TERMINATES THE PROGRAM!
    pass

def SetHelpMessage(programname, overview):
    pass