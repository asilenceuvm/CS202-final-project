
  .globl times
times:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14


  jmp times_start
label_903:
  movq %rdx, %rdx
  movq %rdx, %rax
  jmp times_conclusion
label_904:
  leaq times(%rip), %rcx
  movq $1, %r8
  negq %r8
  movq %rdi, %rdi
  addq %r8, %rdi
  movq %rdx, %rdx
  addq %rsi, %rdx
  movq %rdi, %rdi
  movq %rsi, %rsi
  movq %rdx, %rdx
  movq %rcx, %rax
  
  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  jmp *%rax

times_start:
  movq %rdi, %rdi
  movq %rsi, %rsi
  movq %rdx, %rdx
  cmpq $0, %rdi
  je label_903
  jmp label_904
times_conclusion:

  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq

  .globl main
main:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $16384, %rdi
  movq $16, %rsi
  callq initialize
  movq rootstack_begin(%rip), %r15

  jmp main_start
main_start:
  leaq times(%rip), %rcx
  movq $300, %rdi
  movq $2, %rsi
  movq $0, %rdx
  movq %rcx, %rax
  callq *%rax
  jmp main_conclusion
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
