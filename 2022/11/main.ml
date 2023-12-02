open Base
open Stdio

let ( >> ) g f x = f (g x)

type monkey =
  { id : int
  ; items : int list
  ; op : int -> int
  ; strat : int -> int * int
  ; inspections : int
  }

let make_strat (d, t, f) x = if x % d = 0 then t, x else f, x

let instantiate_monkeys input =
  List.map input ~f:(fun (id, items, op, strat_input) ->
      { id; items; op; strat = make_strat strat_input; inspections = 0 })
;;

let apply_monkey_strat modulo relief monkeys { id; items; op; strat; inspections = _ } =
  let transfers =
    items |> (List.map ~f:(op >> relief >> fun x -> x % modulo) >> List.map ~f:strat)
  in
  let updated_monkeys =
    List.map monkeys ~f:(fun monkey ->
        if monkey.id = id
        then
          { monkey with
            inspections = monkey.inspections + List.length transfers
          ; items = []
          }
        else monkey)
  in
  List.fold transfers ~init:updated_monkeys ~f:(fun acc_monkeys (transfer_id, value) ->
      List.map acc_monkeys ~f:(fun monkey ->
          if monkey.id = transfer_id
          then { monkey with items = value :: monkey.items }
          else monkey))
;;

let round modulo relief monkeys =
  let updated_monkeys, _ =
    List.fold_map
      (List.map monkeys ~f:(fun monkey -> monkey.id))
      ~init:monkeys
      ~f:(fun updated_monkeys monkey_id ->
        let monkey = List.find_exn updated_monkeys ~f:(fun m -> m.id = monkey_id) in
        apply_monkey_strat modulo relief updated_monkeys monkey, monkey.id)
  in
  updated_monkeys
;;

let apply n ~f ~item = List.fold (List.init n ~f:Fn.id) ~init:item ~f:(fun acc _ -> f acc)

let monkey_business_level modulo relief n_rounds monkeys =
  let after_n_rounds = apply n_rounds ~f:(round modulo relief) ~item:monkeys in
  let inspections =
    List.map after_n_rounds ~f:(fun m -> m.id, m.inspections)
    |> List.sort ~compare:(fun a b -> Int.compare (snd b) (snd a))
  in
  match inspections with
  | a :: b :: _ ->
    ( List.map after_n_rounds ~f:(fun m -> m.inspections)
      |> List.sexp_of_t Int.sexp_of_t
      |> Sexp.to_string
    , snd a * snd b )
  | _ -> failwith ""
;;

let () =
  let input_monkeys =
    [ 0, [ 77; 69; 76; 77; 50; 58 ], (fun x -> x * 11), (5, 1, 5)
    ; 1, [ 75; 70; 82; 83; 96; 64; 62 ], (fun x -> x + 8), (17, 5, 6)
    ; 2, [ 53 ], (fun x -> x * 3), (2, 0, 7)
    ; 3, [ 85; 64; 93; 64; 99 ], (fun x -> x + 4), (7, 7, 2)
    ; 4, [ 61; 92; 71 ], (fun x -> x * x), (3, 2, 3)
    ; 5, [ 79; 73; 50; 90 ], (fun x -> x + 2), (11, 4, 6)
    ; 6, [ 50; 89 ], (fun x -> x + 3), (13, 4, 3)
    ; 7, [ 83; 56; 64; 58; 93; 91; 56; 65 ], (fun x -> x + 5), (19, 1, 0)
    ]
  in
  let monkeys = instantiate_monkeys input_monkeys in
  let modulo =
    List.fold input_monkeys ~init:1 ~f:(fun acc (_, _, _, (x, _, _)) -> acc * x)
  in
  let () = printf "\n" in
  let printresult part_number relief n_rounds =
    let s, d = monkey_business_level modulo relief n_rounds monkeys in
    printf "Part %d: %d %s\n" part_number d s
  in
  let () = printresult 1 (fun x -> x / 3) 20 in
  let () = printresult 2 (fun x -> x) 10000 in
  ()
;;
