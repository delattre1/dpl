receita Main() {
  // All bool and int operations
  ingrediente uva, limao : i32;

  ingrediente copo1, copo2 : i32;

  uva recebe 99;
  limao recebe (uva ehIgualzinho 99);

  mostra(uva);
  mostra(limao);

  mostra(uva com limao); // 100
  mostra(uva sem limao); // 98
  mostra(uva multiplicadoPor limao);
  mostra(uva divididoPor limao);
  mostra(uva ehIgualzinho limao);
  mostra(uva temMenosQue limao);
  mostra(uva temMaisQue limao);
  mostra("Agua com limao é bom");

  copo1 recebe 0;
  copo2 recebe 10;

  enquanto (copo1 temMenosQue copo2) {
    mostra(copo1);
    copo1 recebe copo1 com 1;
  }

  ingrediente laranja : i32;
  laranja recebe entrada();

  se (laranja temMaisQue 10) {
    mostra(boloDeBanana(10));
  }

  casoContrario {
    mostra(saladaDeFrutas(70, 7));
  }
}

receita boloDeBanana(banana: i32) -> i32 {
  resultado 8000;
}

receita saladaDeFrutas(banana: i32, maca: i32) -> i32 {
  resultado banana com maca;
}