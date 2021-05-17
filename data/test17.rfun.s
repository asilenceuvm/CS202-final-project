
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
label_41:
  movq %rcx, %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_42:
  movq %rdx, %rdx
  movq %rdx, %rax
  jmp main_conclusion
main_start:
  movq $5, %rcx
  movq $7, %rdx
  movq $5, %rax
  cmpq $6, %rax
  je label_41
  jmp label_42
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
