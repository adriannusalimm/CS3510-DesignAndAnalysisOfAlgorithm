Group Members

Ali Kazmi, akazmi30@gatech.edu
Adrian Nusalim, anusalim3@gatech.edu
Matthew Fishel, mfishel7@gatech.edu

Date Submitted: May 2, 2021

File Submissions:

ALGO1_safe_squares.py : Our first algorithm, which prioritizes safe squares
ALGO1_safe_squares_init_query.py : A tweak of our first algorithm, which scans
    half the board randomly for 0's before beginning the search. We discuss this script
    in our write-up but it should be considered an addendum to ALGO1.
ALGO2_bomb_blossom.py : Our 2nd algorithm, which prioritizes finding bombs as
    fast as possible. Details are provided in the pdf.

    Additional Files:
        A number of files were generated in order to run batch processes where
        our scripts could be applied to multiple boards while data is collected.
        These files are included for demonstration of our process. They are not
        required to run the main algorithm scripts.

        average.py : condenses output text files to produce averaged data from
            board sets of the same shape
        generateAveragedFiles.bash : A batch script which calls average.py for
            all the output text files
        runDensityTrials.bash : calls a designated algorithm script on all provided
            boards of varied density
        runSizeTrials.bash : calls a designated algorithm script on all provided
            boards of varied size
        scaling-plots.ipynb : generates plots from the collected data
        varied_density_output.txt : the unformatted output data collected by runDensityTrials.bash
        varied_size_output.txt : the unformatted output data collected by runSizeTrials.bash

Running Our Files:

Run any algorithm script e.g. ALGO1_safe_squares.py or ALGO2_bomb_blossom.py from the terminal as:

    ALGO1_safe_squares.py <board_json_relative_filepath>

For a more verbose and informative terminal output, include a '1' as a 2nd command line parameter:

    ALGO1_safe_squares.py <board_json_relative_filepath> 1

Limitations:

Our implementation makes no use of the starter as this was not required. We chose to collect data
directly. Consequently, our algorithm files are not expected to work with the starter code. They
should be run on their own from the command line as described.
