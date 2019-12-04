#!/usr/bin/env dart

import 'package:args/args.dart';
import './reverse.dart';

void main(List<String> args) {
  // Do something random with package, relative imports.
  final ArgParser parser = new ArgParser();
  parser.parse(args);
  print(reverse(args[0], ''));
}
