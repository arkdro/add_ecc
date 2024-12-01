
# Add Reed-Solomon ECC to the input data

# Notes

- The program reads the whole input data into memory. If the data is big, it can pose a problem.
- The percentage is calculated quite roughly for edge cases
  (bigger than 12700%, which corresponds about 127 times of the input data. Why do you even need that much?)

# Usage

```
cat xxxxx | add_ecc.py -r 100 | base32 -w 24 | sed -e 's/\(.\)/\1\1\1 /g'
```
