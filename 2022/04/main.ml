open Base
open Stdio

let ( >> ) g f x = f (g x)

let to_pair = function
  | [ a; b ] -> a, b
  | _ -> failwith "not gonna happen"
;;

let split_to_int str =
  str |> (String.split ~on:'-' >> List.map ~f:Int.of_string >> to_pair)
;;

let get_ranges line = line |> (String.split ~on:',' >> List.map ~f:split_to_int >> to_pair)
let are_full_overlap ((a, b), (c, d)) = (a <= c && b >= d) || (c <= a && d >= b)

let partial_overlap ((a, b), (c, d)) =
  are_full_overlap ((a, b), (c, d)) || (a <= c && b <= d && c <= b) || (c <= a && d <= b && a <= d)
;;

(*
- partial overlaps
  a     b
     c     d
---------------
    a      b
  c    d
---------------
- full overlaps
    a    b
    c    d
----------------
    a      b
      c   d
----------------
    a  b
   c     d
*)

let () =
  let lines = In_channel.input_lines In_channel.stdin in
  (* Part 1. For each line, parse 2 pairs of numbers, identify if one overlaps the other. Count the overlaps. *)
  let () =
    lines
    |> List.map ~f:get_ranges
    |> List.count ~f:are_full_overlap
    |> printf "\nPart 1: %d\n"
  in
  let () =
    lines
    |> List.map ~f:get_ranges
    |> List.count ~f:partial_overlap
    |> printf "Part 2: %d\n"
  in
  ()
;;
