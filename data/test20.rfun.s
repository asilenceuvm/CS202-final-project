
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
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15

  jmp main_start
label_102:
  movq free_ptr(%rip), %rdx
  addq $32, free_ptr(%rip)
  movq %rdx, %r11
  movq $135, 0(%r11)
  movq %rdx, %r11
  movq %r12, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq -8(%r15), %r11
  movq 24(%r11), %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_103:
  movq $0, %rdx
  jmp label_102
label_104:
  movq %r15, %rdi
  movq $32, %rsi
  callq collect
  jmp label_102
label_105:
  movq free_ptr(%rip), %rdx
  addq $32, free_ptr(%rip)
  movq %rdx, %r11
  movq $7, 0(%r11)
  movq %rdx, %r11
  movq %r13, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 24(%r11)
  movq $0, %rcx
  movq %rdx, -8(%r15)
  movq $4, %r12
  movq $5, %rbx
  movq -8(%r15), %rax
  movq %rax, -16(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $32, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_103
  jmp label_104
label_106:
  movq $0, %rdx
  jmp label_105
label_107:
  movq %r15, %rdi
  movq $32, %rsi
  callq collect
  jmp label_105
main_start:
  movq $1, %r13
  movq $2, %rbx
  movq $3, %r12
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $32, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_106
  jmp label_107
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $0, %rsp
  subq $16, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
