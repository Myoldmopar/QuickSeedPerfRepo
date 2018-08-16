# -*- coding: utf-8 -*-
import datetime

import pint_var


def create_from_pm_import(properties, limit=False, debug_print=False):

    # This list should cover the core keys coming from PM, ensuring that they map easily
    # We will also look for keys not in this list and just map them to themselves
    pm_key_to_column_heading_map = {
        u'address_1': u'Address',
        u'city': u'City',
        u'state_province': u'State',
        u'postal_code': u'Zip',
        u'county': u'County',
        u'country': u'Country',
        u'property_name': u'Property Name',
        u'property_id': u'Property ID',
        u'year_built': u'Year Built',
    }

    # We will also create a list of values that are used in PM export to indicate a value wasn't available
    # When we import them into SEED here we will be sure to not write those values
    pm_flagged_bad_string_values = [
        u'Not Available',
        u'Unable to Check (not enough data)',
        u'No Current Year Ending Date',
    ]

    # We will make a pass through the first property to get the list of unexpected keys
    for pm_property in properties:
        for pm_key_name, _ in pm_property.iteritems():
            if pm_key_name not in pm_key_to_column_heading_map:
                pm_key_to_column_heading_map[pm_key_name] = pm_key_name
        break

    # Create the header row of the csv file first
    rows = []
    this_row = []
    for _, csv_header in pm_key_to_column_heading_map.iteritems():
        this_row.append(csv_header)
    rows.append(this_row)

    num_properties = len(properties)
    property_num = 0
    last_time = datetime.datetime.now()

    if debug_print:
        print("About to try to import %s properties from ESPM" % num_properties)
        print("Starting at %s" % last_time)

    # Create a single row for each building
    for pm_property in properties:

        # temporarily stop at 10 properties, make this a background task with progress bar so we don't hit a timeout
        if limit and property_num > 10:
            break

        # report some helpful info
        property_num += 1
        if debug_print:
            if property_num / 10.0 == property_num / 10:
                new_time = datetime.datetime.now()
                print("On property number %s; current time: %s" % (property_num, new_time))

        this_row = []

        # Loop through all known PM variables
        for pm_variable, _ in pm_key_to_column_heading_map.iteritems():

            # Initialize this to False for each pm_variable we will search through
            added = False

            # Check if this PM export has this variable in it
            if pm_variable in pm_property:

                # If so, create a convenience variable to store it
                this_pm_variable = pm_property[pm_variable]

                # Next we need to check type.  If it is a string, we will add it here to avoid parsing numerics
                # However, we need to be sure to not add the flagged bad strings.
                # However, a flagged value *could* be a value property name, and we would want to allow that
                if isinstance(this_pm_variable, basestring):
                    if pm_variable == u'property_name':
                        this_row.append(this_pm_variable)
                        added = True
                    elif this_pm_variable not in pm_flagged_bad_string_values:
                        this_row.append(this_pm_variable)
                        added = True

                # If it isn't a string, it should be a dictionary, storing numeric data and units, etc.
                else:

                    # As long as it is a valid dictionary, try to get a meaningful value out of it
                    if '#text' in this_pm_variable and this_pm_variable['#text'] != 'Not Available':

                        # Coerce the value into a proper set of Pint units for us
                        new_var = pint_var.get_pint_var_from_pm_value_object(this_pm_variable)
                        if new_var['success']:
                            pint_value = new_var['pint_value']
                            this_row.append(pint_value.magnitude)
                            added = True
                            # TODO: What to do with the pint_value.units here?

            # And finally, if we haven't set the added flag, give the csv column a blank value
            if not added:
                this_row.append(u'')

        # Then add this property row of data
        rows.append(this_row)

    return rows
