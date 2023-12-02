open Base
open Stdio

type ftree =
  | File of (string * int)
  | Dir of (string * ftree list)

let mkdir name = Dir (name, [])
let touch name size = File (name, size)

let rec insert dir path item =
  match dir with
  | File _ -> failwith "Can't insert inside file"
  | Dir (dir_name, dir_list) ->
    (match path with
    | [] -> Dir (dir_name, item :: dir_list)
    | hd :: tl ->
      Dir
        ( dir_name
        , List.map dir_list ~f:(fun dir_item ->
              match dir_item with
              | File _ -> dir_item
              | Dir (n, _) ->
                if String.( = ) hd n then insert dir_item tl item else dir_item) ))
;;

type command =
  | Chdir of string (* cd <name> *)
  | Updir (* cd .. *)
  | Ignore (* ls *)
  | Mkdir of string (* dir <name> *)
  | Touch of string * int (* <size> <name> *)

let command_of_str str =
  let split = String.split ~on:' ' str in
  match split with
  | a :: b :: tl ->
    if String.( = ) a "$"
    then (
      match b with
      | "cd" ->
        let hd = List.hd_exn tl in
        if String.( = ) hd "/"
        then Ignore
        else if String.( = ) hd ".."
        then Updir
        else Chdir hd
      | "ls" -> Ignore
      | _ -> failwith "not gonna happen")
    else if String.( = ) a "dir"
    then Mkdir b
    else Touch (b, Int.of_string a)
  | _ -> failwith "hopefully not gonna happen"
;;

let create_file_tree root_name commands =
  let root = mkdir root_name in
  let r, _ =
    List.fold commands ~init:(root, []) ~f:(fun (r, path) e ->
        match e with
        | Ignore -> r, path
        | Chdir str -> r, str :: path
        | Updir -> r, List.tl_exn path
        | Mkdir name -> insert r (List.rev path) (mkdir name), path
        | Touch (name, size) -> insert r (List.rev path) (touch name size), path)
  in
  r
;;

let collect_dir_sizes ft =
  let rec iter (res, total) ft =
    match ft with
    | File (_, s) -> [], s
    | Dir (_, l) ->
      let items = List.map l ~f:(fun item -> iter (res, total) item) in
      let res, sum =
        List.fold items ~init:(res, 0) ~f:(fun (a, b) (x, y) -> a @ x, b + y)
      in
      sum :: res, sum
  in
  iter ([], 0) ft
;;

let size_to_delete dir_sizes required =
  List.hd_exn
    (List.filter (List.sort ~compare:Int.compare dir_sizes) ~f:(( <= ) required))
;;

let () =
  let input_lines = In_channel.input_lines In_channel.stdin in
  let commands = List.map ~f:command_of_str input_lines in
  let file_tree = create_file_tree "/" commands in
  let dir_sizes, total_size = collect_dir_sizes file_tree in
  let () =
    dir_sizes
    |> List.filter ~f:(fun x -> x <= 100000)
    |> List.fold ~init:0 ~f:( + )
    |> printf "\nPart 1: %d\n"
  in
  let free = 70000000 - total_size in
  let required = 30000000 - free in
  printf "Part 2: %d" (size_to_delete dir_sizes required);
  printf "\nTotal size: %d" total_size;
  printf "\nRequired: %d" required
;;
