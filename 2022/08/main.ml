open Base
open Stdio

(* let check_visibility trees =
  Array.folding_map trees ~init:(neg 1) ~f:(fun m x ->
      if m < x then x, true else m, false)
;; *)

let ( >> ) g f x = f (g x)
let sum = Array.fold ~init:0 ~f:( + )
let sum2d = Array.map ~f:sum >> sum
let arr_max = Array.fold ~init:Int.min_value ~f:max
let max2d = Array.map ~f:arr_max >> arr_max

let number_visible_trees forest =
  let m = Array.length forest in
  let n = Array.length forest.(0) in
  let visibility = Array.make_matrix ~dimx:m ~dimy:n 0 in
  let () =
    for i = 0 to m - 1 do
      let ml = ref (neg 1) in
      for j = 0 to n - 1 do
        let h = forest.(i).(j) in
        if !ml < h
        then (
          visibility.(i).(j) <- 1;
          ml := h)
      done
    done
  in
  let () =
    for i = 0 to m - 1 do
      let mr = ref (neg 1) in
      for j = n - 1 downto 0 do
        let h = forest.(i).(j) in
        if !mr < h
        then (
          visibility.(i).(j) <- 1;
          mr := h)
      done
    done
  in
  let () =
    for j = 0 to n - 1 do
      let mt = ref (neg 1) in
      for i = 0 to m - 1 do
        let h = forest.(i).(j) in
        if !mt < h
        then (
          visibility.(i).(j) <- 1;
          mt := h)
      done
    done
  in
  let () =
    for j = 0 to n - 1 do
      let mb = ref (neg 1) in
      for i = m - 1 downto 0 do
        let h = forest.(i).(j) in
        if !mb < h
        then (
          visibility.(i).(j) <- 1;
          mb := h)
      done
    done
  in
  sum2d visibility
;;

let count_visible h trees =
  let _, count =
    Array.fold trees ~init:(false, 0) ~f:(fun (d, c) t ->
        if not d then if t < h then false, c + 1 else true, c + 1 else d, c)
  in
  count
;;

let rev arr =
  let arr = Array.copy arr in
  let () = Array.rev_inplace arr in
  arr
;;

let get_column_trees forest j = Array.map forest ~f:(Fn.flip Array.get j)

let score_of_scenic_tree forest =
  let m = Array.length forest in
  let n = Array.length forest.(0) in
  let scores = Array.make_matrix ~dimx:m ~dimy:n 0 in
  let () =
    for i = 1 to m - 2 do
      for j = 1 to n - 2 do
        let row_trees = forest.(i) in
        let column_trees = get_column_trees forest j in
        let right_trees = Array.sub ~pos:(j + 1) ~len:(n - 1 - j) row_trees in
        let left_trees = (Array.sub ~pos:0 ~len:j >> rev) row_trees in
        let bottom_trees = Array.sub ~pos:(i + 1) ~len:(m - 1 - i) column_trees in
        let top_trees = (Array.sub ~pos:0 ~len:i >> rev) column_trees in
        let h = forest.(i).(j) in
        let l = count_visible h left_trees in
        let r = count_visible h right_trees in
        let t = count_visible h top_trees in
        let b = count_visible h bottom_trees in
        scores.(i).(j) <- l * r * t * b
      done
    done
  in
  max2d scores
;;

(* There is actually no need for the [( + ) (neg 48)] when converting the char to number
   because we don't need to actual magnitude. We only need to relative magnitudes when
   comparing the trees for both problems. *)
let parse_line =
  String.to_list >> List.map ~f:(Char.to_int >> ( + ) (neg 48)) >> Array.of_list
;;

let () =
  let lines = In_channel.input_lines In_channel.stdin |> Array.of_list in
  let forest = Array.map lines ~f:parse_line in
  let () = printf "\n" in
  let () = printf "Part 1: %d\n" (number_visible_trees forest) in
  let () = printf "Part 2: %d\n" (score_of_scenic_tree forest) in
  ()
;;
