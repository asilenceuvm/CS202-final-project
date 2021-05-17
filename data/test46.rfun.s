
  .globl fib
fib:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14


  jmp fib_start
label_1439:
  movq $2, %rdx
  movq %rdx, %rax
  jmp fib_conclusion
label_1440:
  movq $1, %rdx
  negq %rdx
  movq %rbx, %rcx
  addq %rdx, %rcx
  leaq fib(%rip), %rdx
  movq %rcx, %rdi
  movq %rdx, %rax
  callq *%rax
  movq %rax, %r12
  movq $2, %rdx
  negq %rdx
  movq %rbx, %rcx
  addq %rdx, %rcx
  leaq fib(%rip), %rdx
  movq %rcx, %rdi
  movq %rdx, %rax
  callq *%rax
  movq %rax, %rdx
  movq %r12, %rcx
  addq %rdx, %rcx
  movq %rcx, %rax
  jmp fib_conclusion
label_1441:
  movq $1, %rdx
  movq %rdx, %rax
  jmp fib_conclusion
label_1442:
  cmpq $1, %rbx
  je label_1439
  jmp label_1440
fib_start:
  movq %rdi, %rbx
  cmpq $0, %rbx
  je label_1441
  jmp label_1442
fib_conclusion:

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
  leaq fib(%rip), %rdx
  movq $15, %rdi
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
