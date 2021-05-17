
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
label_35:
  movq $5, %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_36:
  movq $10, %rdx
  movq %rdx, %rax
  jmp main_conclusion
main_start:
  movq $5, %rdx
  addq $6, %rdx
  cmpq $7, %rdx
  je label_35
  jmp label_36
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
