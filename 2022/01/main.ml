open Base
open Stdio

let sum = List.fold ~init:0 ~f:( + )

let process part =
  let lines = String.split_lines part in
  List.map lines ~f:Int.of_string |> sum
;;

let () =
  let input = In_channel.input_all In_channel.stdin in
  let parts = Str.split (Str.regexp "\n\n") input in
  let () =
    List.fold parts ~init:0 ~f:(fun curr_max part -> max curr_max (process part))
    |> printf "\npart1: %d\n"
  in
  List.map parts ~f:process
  |> List.sort ~compare:(Fn.flip Int.compare)
  |> (Fn.flip List.take) 3
  |> sum
  |> printf "part2: %d\n"
;;
