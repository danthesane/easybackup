Hi. I'm Daniel James, and I began this project in order to easily copy saved games from certain directories onto a backup disk.
As with many things, it has grown as the need for greater functionality has become apparent. However, it will
always function as a quick and easy single-command backup system that is moderately configurable.

As a program, all it does is accept a series of origin paths, either files or directories, and copies them
to a series of destination directories. As of the original commit, it copies every origin path to every destination.

In the future, I plan to add copy-paste functionality that will allow it to read from the clipboard, so that
onerously-long paths will not require typing to input. It would also be nice to eventually implement individual
backup profiles, such as a list of savegame paths copied to a 'savedgames' directory, while financial spreadsheets
are copied to a separate document folder, all with one command.

For now, the next step before development goes any farther is to implement proper logging code to properly handle
exceptions and so forth.
