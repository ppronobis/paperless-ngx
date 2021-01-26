import { Injectable } from '@angular/core';
import { DirtyCheckGuard } from '@ngneat/dirty-check-forms';
import { Observable, Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ConfirmDialogComponent } from 'src/app/components/common/confirm-dialog/confirm-dialog.component';

@Injectable({ providedIn: 'root' })
export class FormDirtyGuard extends DirtyCheckGuard {
  constructor(private modalService: NgbModal) {
    super();
  }

  confirmChanges(): Observable<boolean> {
    let modal = this.modalService.open(ConfirmDialogComponent, {backdrop: 'static'})
    modal.componentInstance.title = $localize`Confirm`
    modal.componentInstance.messageBold = $localize`You have unsaved changes.`
    modal.componentInstance.message = $localize`Are you sure you want to leave?`
    modal.componentInstance.btnClass = "btn-warning"
    modal.componentInstance.btnCaption = $localize`Ok`
    modal.componentInstance.confirmClicked.subscribe(() => {
      modal.componentInstance.buttonsEnabled = false
      modal.close()
    })
    const subject = new Subject<boolean>()
    modal.componentInstance.subject = subject
    return subject.asObservable()
  }
}
