#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    
    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()


    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()


    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    
    def dict_instance(self, line):
        """
            Parse input and convert it to
            Dict for do_create
        """
        dict = {}
        for item in line:
            if "=" in item:
                # creating list from value and key
                # if "=" found
                arg = item.split("=")
                key = arg[0]
                value = arg[1]
                if value[0] == '"' == value[-1]:
                    value = value.replace('"', "").replace("_", " ")
                else:
                    try:
                        value = int(value)
                    except Exception:
                        try:
                            value = float(value)
                        except Exception:
                            continue
                dict[key] = value
        return dict

    def do_create(self, args):
        """ Create an object of any class"""
        args = args.split()
        if not args[0]:
            print("** class name missing **")
            return
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        # creating a dict from args
        new = self.dict_instance(args[1:])
        # sending args on form of kwargs
        new_instance = HBNBCommand.classes[args[0]](**new)
        print(new_instance.id)
        new_instance.save()

    

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")


    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)


    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] is '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] is not ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] is '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
