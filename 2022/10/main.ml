open Base
open Stdio

type instruction =
  | Noop
  | AddX of int

let instruction_of str =
  match str with
  | "noop" -> Noop
  | _ -> String.split ~on:' ' str |> List.last_exn |> Int.of_string |> fun v -> AddX v
;;

let parse_instructions = List.map ~f:instruction_of

(* [process instructions] returns a list of signals that maps cycle number and value in the X registry. *)
let process instructions =
  let signals, _, _ =
    List.fold instructions ~init:([], 1, 0) ~f:(fun (signals, x, count) ins ->
        match ins with
        | Noop -> (count + 1, x) :: signals, x, count + 1
        | AddX v -> (count + 2, x) :: (count + 1, x) :: signals, x + v, count + 2)
  in
  signals
;;

(* Depending on the value in registry X and cycle count, the pixel is filled or not. *)
let render signals =
  List.map (List.rev signals) ~f:(fun (cycle, x) ->
      let cx = cycle % 40 in
      (* Extra +1 for the range because position of the sprite (X) is 0-indexed. *)
      cycle, x - 1 + 1 <= cx && cx <= x + 1 + 1)
;;

let draw rendered_signals =
  List.map rendered_signals ~f:(fun (cycle, active) ->
      String.concat
        ~sep:""
        [ (if active then "#" else "."); (if cycle % 40 = 0 then "\n" else "") ])
  |> String.concat ~sep:""
;;

let signal_strength cycle signals =
  List.find signals ~f:(fun (cn, _) -> cn = cycle)
  |> Option.value ~default:(0, 0)
  |> fun (c, x) -> c * x
;;

let () =
  let lines = In_channel.input_lines In_channel.stdin in
  let instructions = parse_instructions lines in
  let signals = process instructions in
  let interesting_signals = [ 20; 60; 100; 140; 180; 220 ] in
  let () =
    printf
      "\nPart 1: %d\n"
      (List.fold
         ~init:0
         ~f:( + )
         (List.map interesting_signals ~f:(fun cn -> signal_strength cn signals)))
  in
  let () = draw (render signals) |> printf "Part 2:\n%s\n" in
  ()
;;
