open Base
open Stdio

let coord_of_id m id = id / m, id % m
let id_of_coord m (i, j) = (i * m) + j

let potential_dests m id =
  let i, j = coord_of_id m id in
  let coords = [ i - 1, j; i + 1, j; i, j - 1; i, j + 1 ] in
  List.map coords ~f:(id_of_coord m)
;;

let make_grid str =
  let (n, s, e), l =
    String.to_list str
    |> List.fold_map ~init:(0, -1, -1) ~f:(fun (i, s, e) c ->
           match c with
           | 'S' -> (i + 1, i, e), Char.to_int 'a'
           | 'E' -> (i + 1, s, i), Char.to_int 'z'
           | _ -> (i + 1, s, e), Char.to_int c)
  in
  Array.of_list l, n, s, e
;;

let make_graph str m =
  let cells, n, s, e = make_grid str in
  let g = Array.create ~len:n [] in
  let () =
    for i = 0 to n - 1 do
      let h = cells.(i) in
      let valid_dest d = 0 <= d && d < n && cells.(d) - h <= 1 in
      g.(i) <- List.filter (potential_dests m i) ~f:valid_dest
    done
  in
  g, n, s, e
;;

let make_long_string = String.concat ~sep:""

let rec whiletrue pred func result =
  if pred result then whiletrue pred func (func result) else result
;;

let get_path parent e =
  let pred (x, _) = not (parent.(x) = ~-1) in
  let func (x, path) = parent.(x), parent.(x) :: path in
  snd (whiletrue pred func (e, [ e ]))
;;

let bfs g s e =
  let q = Queue.singleton s in
  let n = Array.length g in
  let visited = Array.create ~len:n false in
  let parent = Array.create ~len:n (neg 1) in
  let () = visited.(s) <- true in
  let pred (is_done, _) = not is_done in
  let func (_, _) =
    let x = Queue.dequeue_exn q in
    if x = e
    then true, true
    else (
      let adj = g.(x) in
      let () =
        List.iter adj ~f:(fun v ->
            if not visited.(v)
            then (
              visited.(v) <- true;
              Queue.enqueue q v;
              parent.(v) <- x)
            else ())
      in
      if Queue.is_empty q then true, false else false, false)
  in
  let _, has_path = whiletrue pred func (false, false) in
  if has_path then Some (get_path parent e) else None
;;

let () =
  let lines = In_channel.input_lines In_channel.stdin in
  let modulo = String.length (List.hd_exn lines) in
  let str = make_long_string lines in
  let g, _, s, e = make_graph str modulo in
  let path_length g s e =
    match bfs g s e with
    | None -> Int.max_value
    | Some path -> List.length path - 1
  in
  let () = printf "\nPart 1: %d\n" (path_length g s e) in
  (* The following for part 2. *)
  let start_list =
    let chars = String.to_list str in
    List.filter_mapi chars ~f:(fun i c -> if Char.( = ) c 'a' then Some i else None)
  in
  let lengths = List.map start_list ~f:(fun s -> path_length g s e) in
  let () = printf "Part 2: %d\n" (List.fold lengths ~init:Int.max_value ~f:min) in
  ()
;;
