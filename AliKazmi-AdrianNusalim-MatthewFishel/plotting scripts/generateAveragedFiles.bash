rm averaged_density_output_algo1.txt
rm averaged_density_output_algo2.txt
rm averaged_size_output_algo1.txt
rm averaged_size_output_algo2.txt
python average.py varied_density_output_algo1.txt >> averaged_density_output_algo1.txt
python average.py varied_density_output_algo2.txt >> averaged_density_output_algo2.txt
python average.py varied_size_output_algo1.txt >> averaged_size_output_algo1.txt
python average.py varied_size_output_algo2.txt >> averaged_size_output_algo2.txt

echo 'averaged, see output files'
