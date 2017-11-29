# Wrangling-Functions-in-R
Contains small functions in R, that we use to wrangle our datasets. This is a collection of functions which work for any general case of dataframes (numerical, categorical, mixed). Functional arguments need to be assigned based on specific data structures. Each of these functions have been developed and tested in a standalone R X64 environment. Using these functions does not require the support of any other R package. In this entire document, "d" stands to indicate any dataframe in general.


#### Function 1: cleanBlanck(d)
**Task:** Cleans blank spaces from a dataframe.
>**Example:**
```d = cleanBlanck(d)```

#### Function 2: remEmpty(d)
**Task:** Removes empty columns from a dataframe.
**Example:**
```d = remEmpty(d)```

#### Function 3: changeName(d, header, new_name)
**Task:** Changes name of a header.
>**Example:**
```d = changeName(d, header = "Voltage (V)", new_name = "voltage_v")```

#### Function 4: reScale(d, header, scaling_factor)
**Task:** Rescales a specified numerical header.
>**Example:**
```d = reScale(d, header = "inductance_mohm", scaling_factor = 10)```

#### Function 5: convertNumExt(d, header, ext)
**Task:** Removes a specifieed character extension from a header, and converts to numeric.
>**Example:**
```d = convertNumExt(d, header = "length_mm", ext = " mm")```

#### Function 6: convertCatExt(d, header, ext)
**Task:** Removes a specified character extension from a header, but preserves categorical format.
>**Example:**
```d = convertCatExt(d, header = "frequency", ext = " GHz")```

#### Function 7: removeAfter(d, header, separator)
**Task:** Removes extensions AFTER a specified character.
>**Example:**
```d = removeAfter(d, header = "frequencyrange", separator = " ~ ")```

#### Function 8: removeBefore(d, header, separator)
**Task:** Removes extensions BEFORE a specified character.
>**Example:**
```d = removeBefore(d, header = "frequencyrange", separator = " ~ ")```

#### Function 9: sepHeader(d, header, separator)
**Task:** Separates any particular header into two distinct headers. Useful to separate "range" headers.
>**Example:**
```d = sepHeader(d, header = "temperature", separator = " ~ ")```

#### Function 10: converMixedExt(d, header, ext, scaling_factor)
**Task:** Normalizes mixed unit headers into single unit.
>**Example:**
```d = converMixedExt(d, header = "height", ext = c("m", "mm", "cm", "nm"), scaling_factor = c(1000000000, 1000000, 10000000, 1))```
