
import string
import logging      # logging configuration is placed in a package __index__.py


class RunDescriptionObject(object):
    """ Data and functions common to any level: test, group, global run. """

    def Reset(self):
        self.name               = ""
        self.count              = 1
        self.timeout            = None

        self.pre_commands       = []
        self.test_commands      = []
        self.check_commands     = []
        self.post_commands      = []

        self.substitutions      = {}
        self.flat_substitutions = {}


    def __init__(self, name, count = 1, timeout = None):
        self.Reset()
        self.name = name
        self.count = count
        self.timeout = timeout


    def UpdateRunContext(self, context_dictionary):
        """ Looks for existing object members and updates them with values from context_dictionary.
            Other context_dictionary entries are placed into substitutions of the object """
        new_substitutions = {}
        for (name, value) in context_dictionary.iteritems():
            if (getattr(self, name, None) != None):
                setattr(self, name, value)
            else:
                new_substitutions[name] = value
        self.substitutions.update(new_substitutions)


    def ClearSubstitutions(self):
        self.substitutions = {}


    @staticmethod
    def NormalizeCommands(commands):
        """
            Convert all commands to a list of strings or functions
            Rises exception if any command item has an unsupported type
        """
        normalized_commands = [commands] if (not isinstance(commands, list)) else commands
        # Check that each command is of supported type
        for command in normalized_commands:
            if not (isinstance(command, str) or callable(command)):
                raise TypeError("Commands may be single string, function or a list of strings or functions")
        return normalized_commands


    def NormalizeAllCommands(self):
		
        self.pre_commands   = self.NormalizeCommands(self.pre_commands)
        self.test_commands = self.NormalizeCommands(self.test_commands)
        self.check_commands = self.NormalizeCommands(self.check_commands)
        self.post_commands = self.NormalizeCommands(self.post_commands)


    @staticmethod
    def RaiseIfRecursiveSubstitution(key, text):
        """ Check whether substitution is recursive """
        pattern = "${" + key + "}"
        if (pattern in text):
            raise KeyError("Recursive substitution is detected for %s => %s".format(key, text))


    @staticmethod
    def FlattenSubstitutions(substitutions):
        """
            Substitute iteratively every substitution entry
            Performs substitutions iteratively until there is nothing to substitute or it appears recursive
        """
        iteration_counter = 0
        flatten_substitutions = {}
        for (key, text) in substitutions.iteritems():
            # If iteration number exceeds len(substitutions) then
            # it is likely that some substitutions are recursive
            for iteration_counter in range(len(substitutions)):
                RunDescriptionObject.RaiseIfRecursiveSubstitution(key, text)
                try:
                    text_template = string.Template(text)
                    flatten_text = text_template.substitute(**substitutions)
                except KeyError as e:
                    raise KeyError("No substitution for ${%s} is found".format(e.args[0]))
                if (flatten_text == text):
                    break
                text = flatten_text
                logging.debug("Substitution ${{{}}} iteration {}".format(key, iteration_counter))
                logging.debug(flatten_text)
            flatten_substitutions[key] = flatten_text
        return flatten_substitutions


    def InitFlatSubstitutions(self):
        logging.info("{}.{}".format(self.name, __name__))
        self.flat_substitutions = self.FlattenSubstitutions(self.substitutions)


