## THIS FOLDER
> <br>
>
> - This folder contains the .xlsx files you wish to list as active.
> - The name of the file (without the extension) is used as the descriptor in the
> dropdown list.  It is helpful to include the event date in the filename.
>
> <br>

## EXAMPLE
> <br>
>
> - This folder contains a blank version of the .xlsx files.
> - This template MUST BE USED in order for the code to function.
> - Modifications such as increasing rows on the start list are fine.
> - This folder also includes a dummy event for reference.
>
> <br>

## ARCHIVE
> <br>
>
> - If a event is no longer to be listed we recommend moving to this folder.
>
> <br>

## PENDING
> <br>
>
> - This folder can be used to hold events which have been set up, but should
> not yet be live for registration.
>  To make the event live, simply move it into the 'events' parent folder.
>
> <br>

### Moving Files
> <br>
>
> - In order to move files between folders, open a bash console in the same 
> directory as the file you want to move.
> - Enter into the console
> ```
> mv my_file ~/mysite/O-Book/folder
> ```
> replacing *my_file* with the name of the file, **INCLUDING** the file extension,
> and *folder* the with sub-directory you wish to move it to
>
> - For example, if you wished to archive an event, you would enter
> ```
> mv old_event.xlsx ~/mysite/O-Book/events/archive
> ```	
> - Or if you wanted to make a pending event live, you would enter
> ```
> mv new_event.xlsx ~/mysite/O-Book/events
> ```
>
> <br>
	
