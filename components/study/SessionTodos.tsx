import { useState } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import { Button } from '../approved-ui-runtime';
import { Input } from '../approved-ui-runtime';
import { Checkbox } from '../approved-ui-runtime';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '../approved-ui-runtime';
import type { PlanStep } from '../approved-ui-runtime';
import './study-kobra.css';

export function SessionTodos({
  steps,
  onSave,
  onClose,
}: {
  steps: PlanStep[];
  onSave: (steps: PlanStep[]) => void;
  onClose: () => void;
}) {
  const [draft, setDraft] = useState(() =>
    steps.map((step) => ({ ...step, id: crypto.randomUUID() })),
  );
  const [error, setError] = useState('');
  return (
    <Dialog
      open
      onOpenChange={(open) => {
        if (!open) onClose();
      }}
    >
      <DialogContent className="ks-todo-dialog">
        <form
          onSubmit={(event) => {
            event.preventDefault();
            const cleaned = draft.map(({ label, done }) => ({ label: label.trim(), done }));
            if (cleaned.some((step) => !step.label)) {
              setError('Give each to-do a name, or remove the empty row.');
              return;
            }
            if (new Set(cleaned.map((step) => step.label.toLowerCase())).size !== cleaned.length) {
              setError('Give each to-do a different name so you can tell them apart.');
              return;
            }
            onSave(cleaned);
          }}
        >
          <DialogHeader>
            <DialogTitle>Edit your to-dos</DialogTitle>
            <DialogDescription>
              Make this session your own. Change the list before you begin.
            </DialogDescription>
          </DialogHeader>
          <div className="ks-todo-rows">
            {draft.length === 0 && <p>No to-dos yet. Add one when you’re ready.</p>}
            {draft.map((step, index) => (
              <div className="ks-todo-row" key={step.id}>
                <Checkbox
                  checked={!!step.done}
                  aria-label={`Mark to-do ${index + 1} complete`}
                  onCheckedChange={(done) =>
                    setDraft((items) =>
                      items.map((item) => (item.id === step.id ? { ...item, done: !!done } : item)),
                    )
                  }
                />
                <label>
                  <span>To-do {index + 1}</span>
                  <Input
                    value={step.label}
                    maxLength={160}
                    autoFocus={index === 0}
                    aria-describedby={error ? 'todo-error' : undefined}
                    onChange={(event) => {
                      setError('');
                      setDraft((items) =>
                        items.map((item) =>
                          item.id === step.id ? { ...item, label: event.target.value } : item,
                        ),
                      );
                    }}
                  />
                </label>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  aria-label={`Remove to-do ${index + 1}`}
                  onClick={() => {
                    setError('');
                    setDraft((items) => items.filter((item) => item.id !== step.id));
                  }}
                >
                  <Trash2 />
                </Button>
              </div>
            ))}
          </div>
          <Button
            type="button"
            variant="outline"
            onClick={() => {
              setError('');
              setDraft((items) => [...items, { id: crypto.randomUUID(), label: '', done: false }]);
            }}
          >
            <Plus /> Add a to-do
          </Button>
          {error && (
            <p id="todo-error" className="ks-todo-error" role="alert">
              {error}
            </p>
          )}
          <DialogFooter>
            <Button type="button" variant="ghost" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" variant="outline" className="nsu-ink-outline">
              Save to-dos
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
