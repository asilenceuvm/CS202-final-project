
  .globl m
m:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14


  jmp m_start
m_start:
  movq %rdi, %rdx
  movq %rsi, %rdx
  movq %rdx, %rdx
  movq %rcx, %rdx
  movq %r8, %rdx
  movq %r9, %rdx
  movq %rdx, %r11
  movq 32(%r11), %rdx
  movq %rdx, %rax
  jmp m_conclusion
m_conclusion:

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
  subq $16, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $16384, %rdi
  movq $16, %rsi
  callq initialize
  movq rootstack_begin(%rip), %r15

  jmp main_start
label_1425:
  movq free_ptr(%rip), %r9
  addq $40, free_ptr(%rip)
  movq %r9, %r11
  movq $9, 0(%r11)
  movq %r9, %r11
  movq %rbx, 8(%r11)
  movq $0, %rdx
  movq %r9, %r11
  movq %r12, 16(%r11)
  movq $0, %rdx
  movq %r9, %r11
  movq %r14, 24(%r11)
  movq $0, %rdx
  movq %r9, %r11
  movq -16(%rbp), %rax
  movq %rax, 32(%r11)
  movq $0, %rdx
  movq $777, %rdi
  movq $776, %rsi
  movq $775, %rdx
  movq $774, %rcx
  movq $773, %r8
  movq %r9, %r9
  movq %r13, %rax
  callq *%rax
  jmp main_conclusion
label_1426:
  movq $0, %rdx
  jmp label_1425
label_1427:
  movq %r15, %rdi
  movq $40, %rsi
  callq collect
  jmp label_1425
main_start:
  leaq m(%rip), %r13
  movq $772, %rbx
  movq $771, %r12
  movq $770, %r14
  movq $42, -16(%rbp)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $40, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_1426
  jmp label_1427
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $16, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
