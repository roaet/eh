# Eh

Eh is a tool to give quick help on a particular subject

The source code can be found at:

```
https://github.com/roaet/eh
```

## Installing

Install with `pip install eh`. You may want to use `sudo` if you want it
available everywhere.

With some versions of linux it will install it into `~/.local/bin` when you
do not use `sudo`. Ensure that this directory is in your `PATH` if you want to
run eh.

## Eh Configuration File

The Eh configuration file is located at ~/.eh/eh.ini. This location cannot be
changed.

## Making an eh topic

You can make a new eh topic by:

- contributing to the subject repo at `https://github.com/roaet/eh_subjects`
- creating your own repo and including it in your eh.ini

### Creating a new subject repo

When you add it to your eh.ini you must provide the entire URI. The value on
the left-hand side of the `=` does not matter as long as it is unique to your
configuration file.

## Auto Complete

(shoutout to https://github.com/CarvellScott/completion_utils for the help)

After installing you can add eh bash completion by running: `complete -C eh_autocomplete eh`

## Future features

- Config from home for color options
- Personal subject repositories
