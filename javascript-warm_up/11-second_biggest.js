#!/usr/bin/node

const numbers = process.argv.slice(2).map((value) => parseInt(value));

numbers.sort((a, b) => a - b);

if (numbers.length < 2) {
  console.log(0);
} else {
  console.log(numbers[numbers.length - 2]);
}
