String reverse(String input, String output) {
  if (input.length == 0) {
    return output;
  }

  return reverse(
      input.substring(0, input.length - 1),
      output + input.substring(input.length - 1, input.length));
}
