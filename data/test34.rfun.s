
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
label_919:
  movq $0, %rdx
  movq %rdx, %rax
  jmp times_conclusion
label_920:
  movq $1, %rdx
  negq %rdx
  movq %rcx, %rcx
  addq %rdx, %rcx
  leaq times(%rip), %rdx
  movq %rcx, %rdi
  movq %rbx, %rsi
  movq %rdx, %rax
  callq *%rax
  movq %rax, %rdx
  movq %rbx, %rcx
  addq %rdx, %rcx
  movq %rcx, %rax
  jmp times_conclusion
times_start:
  movq %rdi, %rcx
  movq %rsi, %rbx
  cmpq $0, %rcx
  je label_919
  jmp label_920
times_conclusion:

  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq

  .globl fact
fact:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14


  jmp fact_start
label_921:
  movq $1, %rdx
  movq %rdx, %rax
  jmp fact_conclusion
label_922:
  leaq times(%rip), %rbx
  movq $1, %rdx
  negq %rdx
  movq %r12, %rcx
  addq %rdx, %rcx
  leaq fact(%rip), %rdx
  movq %rcx, %rdi
  movq %rdx, %rax
  callq *%rax
  movq %rax, %rdx
  movq %r12, %rdi
  movq %rdx, %rsi
  movq %rbx, %rax
  
  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  jmp *%rax

fact_start:
  movq %rdi, %r12
  cmpq $0, %r12
  je label_921
  jmp label_922
fact_conclusion:

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
  leaq fact(%rip), %rdx
  movq $5, %rdi
  movq %rdx, %rax
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
