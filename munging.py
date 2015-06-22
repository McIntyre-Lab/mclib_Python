#!/usr/bin/env python
""" A set of common helper function to getting things done quickly and cleanly """


def asList(x):
    """ Convert a variable to a list.

    :param x: an object that you would like to convert to a list. Will raise an
        exception if it is iterable but not already a tuple or list.

    """

    if isinstance(x, list):
        return x
    elif isinstance(x, tuple):
        return list(x)
    elif not hasattr(x, '__iter__'):
        return [x, ]
    else:
        raise ValueError('Could not convert {} to a list'.format(str(x)))


def mergeAndDrop(df, flags, left_on, right_on, flagName, keep_in_list=None, keep_logic=None, all=True):
    """ Merge on a set of flags and drop depending on a criteria.

    Arguments:

        :type df: pandas.DataFrame
        :param df: A data frame that you want to merge flags on to.

        :type flags: pandas.DataFrame
        :param flags: A data frame of flags that you want to merge.

        :param str left_on: Column name that you want to merge in your main data frame.

        :param str right_on: Column name that you want to merge in your flags data frame.

        :param list flagName: Column name with flags.

        :param list keep_in_list: List of what flag values to keep.

        :param str keep_logic: A string with the logical opperator for which
            flags to keep. For example, ('== 0', '<= 1', '>= 10', '!= 2').

        :param bool all: If True then a row will be kept if all flags return
            True. If false, a row will be kept if any of the values were True.

    Returns:

        :return: A data frame without the rows that were flagged
        :rtype: pd.DataFrame

    """

    # Merge datasets
    dfI = df.reset_index()
    flagsI = flags.reset_index()
    merged = dfI.merge(flagsI, how='left', left_on=left_on, right_on=right_on)

    # Make sure flagName is a list
    nameList = asList(flagName)

    # Drop Flags
    if keep_in_list and keep_logic:
        print "keep_in_list and keep_logic are mutually exclusive. Please only provide one."
        raise Exception

    if keep_in_list:
        print "Keeping flags in given list."

        # Make sure keep_in_list is a list
        flagList = asList(keep_in_list)

        # Create mask where drop_when values are False
        cleanMask = merged[nameList].isin(flagList).values

    elif keep_logic:
            cleanMask = eval('merged[nameList] ' + keep_logic).values

    else:
        print "Please provide either a keep_in_list and keep_logic."
        raise Exception

    # Return df with specific rows
    if all:
        return df[cleanMask.all(axis=1)]
    else:
        return df[cleanMask.any(axis=1)]


if __name__ == '__main__':
    pass