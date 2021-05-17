
  .globl main
main:
  pushq %rbp
  movq %rsp, %rbp
  subq $32, %rsp
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
  movq $5, %rcx
  movq $6, %rdi
  movq $7, -16(%rbp)
  movq $8, %r9
  movq $9, -32(%rbp)
  movq $10, %r14
  movq $11, %r10
  movq $12, %r13
  movq $13, %r8
  movq $14, %rbx
  movq $15, %r12
  movq $16, -24(%rbp)
  movq $17, %rdx
  movq $18, %rsi
  movq %rdx, %rdx
  addq %rsi, %rdx
  movq -24(%rbp), %rsi
  addq %rdx, %rsi
  movq %r12, %rdx
  addq %rsi, %rdx
  movq %rbx, %rsi
  addq %rdx, %rsi
  movq %r8, %rdx
  addq %rsi, %rdx
  movq %r13, %rsi
  addq %rdx, %rsi
  movq %r10, %rdx
  addq %rsi, %rdx
  movq %r14, %rsi
  addq %rdx, %rsi
  movq -32(%rbp), %rdx
  addq %rsi, %rdx
  movq %r9, %rsi
  addq %rdx, %rsi
  movq -16(%rbp), %rdx
  addq %rsi, %rdx
  movq %rdi, %rsi
  addq %rdx, %rsi
  movq %rcx, %rdx
  addq %rsi, %rdx
  movq %rdx, %rax
  jmp main_conclusion
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $32, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
